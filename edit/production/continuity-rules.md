# Production continuity rules

## Locked source handling

- Treat each `source_path` and SHA-256 value in [asset-manifest.json](asset-manifest.json) as immutable. Do not overwrite, rename, or edit a source asset.
- Use `pre-card-hologram-front (1).png` as the sole exact, readable product-card source in final imagery. Generated card artwork may be used only to establish staging, pose, or lighting and must be replaced before delivery.
- Do not use `bc087e2e-1b35-44bf-a25a-0d598ef7482f.png` to establish any character identity.
- The APNG card asset and the 3D hand asset are excluded from the main film.
- `KakaoTalk_20260715_200455753.mp4` is an excluded reference video and cannot be used as footage or a generation reference.

## Scene continuity

- Maintain one locked tourist identity, wardrobe, bag, and suitcase across all tourist shots.
- Maintain one locked referee identity, striped uniform, whistle, watch, and deadpan expression across all referee shots.
- Keep the premium commercial visual treatment consistent: clean transit environment, cool cyan-white light, soft bloom, and subtle grain.
- Preserve story order: initial failed unbranded-card attempt, referee intervention, exact TOSS-card reveal, successful tap, then relief.

## Delivery guardrails

- Do not show the exact TOSS product card before its reveal moment.
- Reject generated text, malformed hands, duplicate limbs, duplicate cards, incorrect product logos, and wardrobe or identity drift.
- Final delivery is a 1080x1920 portrait master at 30 fps.
