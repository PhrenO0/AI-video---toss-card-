# TOSS Japan tourist reel — QA report

## Delivery

- Final: `TOSS_JP_reel_v01.mp4`
- Duration: 12.800 seconds
- Video: H.264, 1080×1920, 30 fps, yuv420p
- Audio: AAC stereo, 48 kHz, 192 kb/s
- File size: 9,578,400 bytes
- SHA-256: `F2D5DF4DC046AFB200BE98E5D32EAF575F0DF036C2A6F1ECAC97E0867AEB005A`

## Creative requirements

- Pass — 9:16, 12–15 second ad format.
- Pass — premium Japanese-commercial look; no smartphone, vlog, selfie, or UGC treatment.
- Pass — Japanese woman, ivory blouse, light-blue jeans, beige crossbody bag, and silver suitcase remain continuous.
- Pass — only an unbranded gray-lilac card appears in the rejected-tap scene.
- Pass — two short apparent gate-error sounds are repeated as two real referee-whistle sounds during the reveal.
- Pass — the same Korean referee walks in, draws one TOSS card, raises it vertically, and taps the gate.
- Pass — success reader uses a green pulse and the gate opens.
- Pass — no spoken dialogue; sparse Japanese SFX captions only.
- Pass — final copy is `韓国の移動は、TOSSカードで。` with small Korean support copy.
- Pass — the end slate uses an exact byte-for-byte copy of the supplied card PNG; SHA-256 match confirmed.

## Technical verification

Fresh automated verification: 15/15 checks passed.

- Full video and audio decode: pass.
- No detected black frames ≥150 ms: pass.
- No detected silence ≥350 ms at −50 dB: pass.
- Integrated loudness: −17.4 LUFS.
- Maximum sample peak: −6.9 dBFS.
- Every recorded Higgsfield image/video job is completed.
- All six accepted source videos and both licensed audio recordings are present.

## Source and rebuild records

- Build script: `../scripts/build_preview.ps1`
- Subtitle source: `../subtitles/toss_jp_v01.ass`
- Higgsfield ledger: `../higgsfield/jobs.json`
- Audio license record: `../audio/LICENSES.md`
- Contact sheet: `TOSS_JP_reel_v01_contact_1fps.png`

Rebuild from the project root with:

```powershell
& 'edit\scripts\build_preview.ps1'
```

Higgsfield credits remaining after delivery: 1036.
