"""SQLite 저장소.

별도 인프라 없이 돌아가야 해서 파일 DB를 쓴다.
중복 수집을 막는 것과, "슬랙에 이미 보낸 건 다시 안 보내는 것"이 핵심 역할.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable, Iterator

from .models import Platform, Reference

SCHEMA = """
CREATE TABLE IF NOT EXISTS refs (
    uid TEXT PRIMARY KEY,
    platform TEXT NOT NULL,
    post_id TEXT NOT NULL,
    url TEXT NOT NULL,
    author TEXT,
    text TEXT,
    created_at TEXT NOT NULL,
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    share_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,
    media_type TEXT,
    media_urls TEXT,
    query TEXT,
    provider TEXT,
    author_follower_count INTEGER DEFAULT 0,
    collected_at TEXT NOT NULL,
    score REAL DEFAULT 0,
    raw TEXT,
    notified_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_refs_created ON refs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_refs_score ON refs(score DESC);
CREATE INDEX IF NOT EXISTS idx_refs_notified ON refs(notified_at);

CREATE TABLE IF NOT EXISTS cardnews (
    slug TEXT PRIMARY KEY,
    topic TEXT,
    spec TEXT NOT NULL,
    status TEXT DEFAULT 'draft',
    figma_node_id TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""

# raw는 용량이 크고 랭킹/표시에 안 쓰이므로 목록 조회에서 제외한다.
_LIST_COLUMNS = (
    "uid, platform, post_id, url, author, text, created_at, like_count, "
    "comment_count, share_count, view_count, media_type, media_urls, query, "
    "provider, author_follower_count, collected_at, score, '{}' AS raw"
)


class Store:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as conn:
            conn.executescript(SCHEMA)

    @contextmanager
    def _conn(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    # ------------------------------------------------------------------ refs
    def upsert_many(self, refs: Iterable[Reference]) -> int:
        """새로 들어온 건수를 반환. 기존 건은 지표/점수만 갱신한다."""
        rows = [r.to_row() for r in refs]
        if not rows:
            return 0
        inserted = 0
        with self._conn() as conn:
            for row in rows:
                existing = conn.execute(
                    "SELECT 1 FROM refs WHERE uid = ?", (row["uid"],)
                ).fetchone()
                if existing:
                    conn.execute(
                        """UPDATE refs SET like_count=:like_count,
                           comment_count=:comment_count, share_count=:share_count,
                           view_count=:view_count, score=:score,
                           collected_at=:collected_at
                           WHERE uid=:uid""",
                        row,
                    )
                else:
                    placeholders = ", ".join(f":{k}" for k in row)
                    conn.execute(
                        f"INSERT INTO refs ({', '.join(row)}) VALUES ({placeholders})",
                        row,
                    )
                    inserted += 1
        return inserted

    def top(
        self,
        limit: int = 10,
        since_hours: int | None = None,
        platform: Platform | str | None = None,
        only_unnotified: bool = False,
    ) -> list[Reference]:
        sql = f"SELECT {_LIST_COLUMNS} FROM refs WHERE 1=1"
        params: list = []
        if since_hours is not None:
            cutoff = datetime.now(timezone.utc) - timedelta(hours=since_hours)
            sql += " AND created_at >= ?"
            params.append(cutoff.isoformat())
        if platform is not None:
            value = platform.value if isinstance(platform, Platform) else str(platform)
            sql += " AND platform = ?"
            params.append(value)
        if only_unnotified:
            sql += " AND notified_at IS NULL"
        sql += " ORDER BY score DESC, created_at DESC LIMIT ?"
        params.append(limit)
        with self._conn() as conn:
            return [Reference.from_row(dict(r)) for r in conn.execute(sql, params)]

    def get(self, uid: str) -> Reference | None:
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM refs WHERE uid = ?", (uid,)).fetchone()
        return Reference.from_row(dict(row)) if row else None

    def mark_notified(self, uids: Iterable[str]) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._conn() as conn:
            conn.executemany(
                "UPDATE refs SET notified_at = ? WHERE uid = ?",
                [(now, uid) for uid in uids],
            )

    def counts_by_platform(self) -> dict[str, int]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT platform, COUNT(*) AS n FROM refs GROUP BY platform"
            ).fetchall()
        return {r["platform"]: r["n"] for r in rows}

    # -------------------------------------------------------------- cardnews
    def save_cardnews(self, slug: str, topic: str, spec_json: str, status: str = "draft") -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._conn() as conn:
            conn.execute(
                """INSERT INTO cardnews (slug, topic, spec, status, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ON CONFLICT(slug) DO UPDATE SET
                     topic=excluded.topic, spec=excluded.spec,
                     status=excluded.status, updated_at=excluded.updated_at""",
                (slug, topic, spec_json, status, now, now),
            )

    def get_cardnews(self, slug: str) -> dict | None:
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM cardnews WHERE slug = ?", (slug,)).fetchone()
        return dict(row) if row else None

    def list_cardnews(self, limit: int = 20) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT slug, topic, status, figma_node_id, created_at "
                "FROM cardnews ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(r) for r in rows]

    def set_cardnews_status(self, slug: str, status: str, figma_node_id: str = "") -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._conn() as conn:
            conn.execute(
                "UPDATE cardnews SET status = ?, figma_node_id = COALESCE(NULLIF(?, ''), figma_node_id), "
                "updated_at = ? WHERE slug = ?",
                (status, figma_node_id, now, slug),
            )
