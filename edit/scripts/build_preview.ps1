$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Invoke-FFmpeg {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)
    & ffmpeg -hide_banner -loglevel error @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "ffmpeg failed with exit code $LASTEXITCODE"
    }
}

$segmentDir = 'edit/assembly/segments'
$audioDir = 'edit/audio/generated'
$previewDir = 'edit/preview'
New-Item -ItemType Directory -Force $segmentDir, $audioDir, $previewDir | Out-Null

$normalizeTail = 'scale=1080:1920:flags=lanczos,fps=30,setsar=1,format=yuv420p'

# 01: Reverse only the valid first 0.55 s so the generic card descends onto the top reader.
Invoke-FFmpeg @(
    '-y', '-i', 'edit/generated/videos/final/shot_01_fail.mp4', '-an',
    '-filter_complex', "[0:v]trim=start=0:end=0.55,reverse,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=0.35,$normalizeTail[v]",
    '-map', '[v]', '-t', '0.90', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-movflags', '+faststart',
    "$segmentDir/01_fail.mp4"
)

# 02: Eye-first puzzled reaction.
Invoke-FFmpeg @(
    '-y', '-i', 'edit/generated/videos/final/shot_02_reaction.mp4', '-an',
    '-filter_complex', "[0:v]trim=start=0:end=1.40,setpts=PTS-STARTPTS,$normalizeTail[v]",
    '-map', '[v]', '-t', '1.40', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-movflags', '+faststart',
    "$segmentDir/02_reaction.mp4"
)

# 03: Compress the two whistle beats into the reveal beat.
Invoke-FFmpeg @(
    '-y', '-i', 'edit/generated/videos/tests/test_whistle.mp4', '-an',
    '-filter_complex', "[0:v]trim=start=0:end=3.0,setpts=(PTS-STARTPTS)/2.3076923077,$normalizeTail[v]",
    '-map', '[v]', '-t', '1.30', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-movflags', '+faststart',
    "$segmentDir/03_whistle.mp4"
)

# 04+05: Full approach, pocket action, and card declaration.
Invoke-FFmpeg @(
    '-y', '-i', 'edit/generated/videos/tests/test_walk_reveal.mp4', '-an',
    '-filter_complex', "[0:v]trim=start=0:end=4.0,setpts=(PTS-STARTPTS)/1.1764705882,$normalizeTail[v]",
    '-map', '[v]', '-t', '3.40', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-movflags', '+faststart',
    "$segmentDir/04_walk_reveal.mp4"
)

# 06: One fast product tap and green response.
Invoke-FFmpeg @(
    '-y', '-i', 'edit/generated/videos/tests/test_success_tap.mp4', '-an',
    '-filter_complex', "[0:v]trim=start=0:end=4.0,setpts=(PTS-STARTPTS)/2.8571428571,$normalizeTail[v]",
    '-map', '[v]', '-t', '1.40', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-movflags', '+faststart',
    "$segmentDir/05_success.mp4"
)

# 07: Keep only the understated bow before the expression becomes too broad.
Invoke-FFmpeg @(
    '-y', '-i', 'edit/generated/videos/final/shot_07_relief.mp4', '-an',
    '-filter_complex', "[0:v]trim=start=0:end=1.20,setpts=PTS-STARTPTS,$normalizeTail[v]",
    '-map', '[v]', '-t', '1.20', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-movflags', '+faststart',
    "$segmentDir/06_relief.mp4"
)

# 08: Exact supplied TOSS card on a clean, premium brand gradient.
Invoke-FFmpeg @(
    '-y',
    '-f', 'lavfi', '-i', 'gradients=s=1080x1920:r=30:d=3.2:c0=0xF9FCFF:c1=0xDCEAFF:x0=160:y0=80:x1=920:y1=1800:seed=11:speed=0',
    '-loop', '1', '-t', '3.2', '-i', 'edit/assets/toss_card_exact.png',
    '-filter_complex', '[1:v]scale=390:-1,format=rgba,fade=t=in:st=0:d=0.25:alpha=1,split=2[card][shadow];[shadow]colorchannelmixer=rr=0:gg=0:bb=0:aa=0.22,boxblur=18:2[sh];[0:v][sh]overlay=x=(W-w)/2+18:y=278:format=auto[bg];[bg][card]overlay=x=(W-w)/2:y=250:format=auto,drawbox=x=100:y=1415:w=880:h=2:color=0x9CB9E6@0.32:t=fill,format=yuv420p[v]',
    '-map', '[v]', '-t', '3.20', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-movflags', '+faststart',
    "$segmentDir/07_end_slate.mp4"
)

# Hard-cut assembly preserves the deadpan comedy rhythm.
Invoke-FFmpeg @(
    '-y',
    '-i', "$segmentDir/01_fail.mp4",
    '-i', "$segmentDir/02_reaction.mp4",
    '-i', "$segmentDir/03_whistle.mp4",
    '-i', "$segmentDir/04_walk_reveal.mp4",
    '-i', "$segmentDir/05_success.mp4",
    '-i', "$segmentDir/06_relief.mp4",
    '-i', "$segmentDir/07_end_slate.mp4",
    '-filter_complex', '[0:v][1:v][2:v][3:v][4:v][5:v][6:v]concat=n=7:v=1:a=0,format=yuv420p[v]',
    '-map', '[v]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-movflags', '+faststart',
    "$previewDir/toss_jp_reel_picture_lock.mp4"
)

# Burn the sparse Japanese SFX captions and final Japanese/Korean card copy only after picture lock.
Invoke-FFmpeg @(
    '-y', '-i', "$previewDir/toss_jp_reel_picture_lock.mp4", '-an',
    '-vf', "subtitles=filename='edit/subtitles/toss_jp_v01.ass'",
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-movflags', '+faststart',
    "$previewDir/toss_jp_reel_text_lock.mp4"
)

# Locally synthesized detail sounds. Every short asset has a 30 ms or shorter edge fade.
Invoke-FFmpeg @(
    '-y', '-f', 'lavfi', '-i', 'sine=frequency=88:duration=0.16:sample_rate=48000',
    '-filter:a', 'volume=0.38,afade=t=in:st=0:d=0.008,afade=t=out:st=0.11:d=0.05',
    '-c:a', 'pcm_s24le', "$audioDir/footstep.wav"
)

Invoke-FFmpeg @(
    '-y', '-f', 'lavfi', '-i', 'anoisesrc=color=white:duration=0.46:sample_rate=48000',
    '-filter:a', 'highpass=f=1200,lowpass=f=9000,volume=0.10,afade=t=in:st=0:d=0.025,afade=t=out:st=0.25:d=0.21',
    '-c:a', 'pcm_s24le', "$audioDir/card_whoosh.wav"
)

Invoke-FFmpeg @(
    '-y',
    '-f', 'lavfi', '-i', 'sine=frequency=880:duration=0.48:sample_rate=48000',
    '-f', 'lavfi', '-i', 'sine=frequency=1320:duration=0.48:sample_rate=48000',
    '-filter_complex', '[0:a]volume=0.14,afade=t=in:st=0:d=0.02,afade=t=out:st=0.28:d=0.20[a0];[1:a]volume=0.08,afade=t=in:st=0:d=0.02,afade=t=out:st=0.22:d=0.26[a1];[a0][a1]amix=inputs=2:normalize=0,aecho=0.8:0.45:55:0.18[out]',
    '-map', '[out]', '-c:a', 'pcm_s24le', "$audioDir/hero_shimmer.wav"
)

Invoke-FFmpeg @(
    '-y',
    '-f', 'lavfi', '-i', 'sine=frequency=1174.66:duration=0.16:sample_rate=48000',
    '-f', 'lavfi', '-i', 'sine=frequency=1567.98:duration=0.25:sample_rate=48000',
    '-filter_complex', '[0:a]volume=0.18,afade=t=in:st=0:d=0.01,afade=t=out:st=0.10:d=0.06[n0];[1:a]volume=0.14,adelay=90|90,afade=t=in:st=0:d=0.01,afade=t=out:st=0.17:d=0.08[n1];[n0][n1]amix=inputs=2:normalize=0,aecho=0.8:0.35:45:0.12[out]',
    '-map', '[out]', '-c:a', 'pcm_s24le', "$audioDir/success_chime.wav"
)

Invoke-FFmpeg @(
    '-y',
    '-f', 'lavfi', '-i', 'sine=frequency=523.25:duration=0.70:sample_rate=48000',
    '-f', 'lavfi', '-i', 'sine=frequency=659.25:duration=0.62:sample_rate=48000',
    '-f', 'lavfi', '-i', 'sine=frequency=783.99:duration=0.54:sample_rate=48000',
    '-filter_complex', '[0:a]volume=0.08,afade=t=in:st=0:d=0.02,afade=t=out:st=0.36:d=0.34[n0];[1:a]volume=0.07,adelay=130|130,afade=t=in:st=0:d=0.02,afade=t=out:st=0.31:d=0.31[n1];[2:a]volume=0.06,adelay=260|260,afade=t=in:st=0:d=0.02,afade=t=out:st=0.26:d=0.28[n2];[n0][n1][n2]amix=inputs=3:normalize=0,aecho=0.8:0.35:75:0.16[out]',
    '-map', '[out]', '-c:a', 'pcm_s24le', "$audioDir/end_resolve.wav"
)

# Final sound design. The same real whistle recording appears twice at the gate and twice with the referee.
Invoke-FFmpeg @(
    '-y',
    '-i', 'edit/audio/sources/mixkit_subway_interior_2680.wav',
    '-i', 'edit/audio/sources/mixkit_police_short_whistle_615.wav',
    '-i', "$audioDir/footstep.wav",
    '-i', "$audioDir/card_whoosh.wav",
    '-i', "$audioDir/hero_shimmer.wav",
    '-i', "$audioDir/success_chime.wav",
    '-i', "$audioDir/end_resolve.wav",
    '-filter_complex', '[0:a]atrim=start=1.0:end=13.8,asetpts=PTS-STARTPTS,highpass=f=70,lowpass=f=8500,volume=0.085,afade=t=in:st=0:d=0.03,afade=t=out:st=12.72:d=0.08[amb];[1:a]atrim=start=0.05:end=0.40,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.008,afade=t=out:st=0.31:d=0.04,asplit=4[w1][w2][w3][w4];[w1]highpass=f=1800,lowpass=f=5600,volume=0.48,adelay=180|180[wa];[w2]highpass=f=1800,lowpass=f=5600,volume=0.48,adelay=570|570[wb];[w3]highpass=f=900,volume=0.72,aecho=0.8:0.35:42:0.12,adelay=2400|2400[wc];[w4]highpass=f=900,volume=0.72,aecho=0.8:0.35:42:0.12,adelay=2800|2800[wd];[2:a]asplit=2[fs1][fs2];[fs1]volume=0.55,adelay=3820|3820[f1];[fs2]volume=0.48,adelay=4480|4480[f2];[3:a]adelay=5450|5450[whoosh];[4:a]adelay=5820|5820[hero];[5:a]adelay=7160|7160[tag];[6:a]adelay=9680|9680[end];[amb][wa][wb][wc][wd][f1][f2][whoosh][hero][tag][end]amix=inputs=11:duration=longest:normalize=0,atrim=start=0:end=12.8,afade=t=in:st=0:d=0.03,afade=t=out:st=12.74:d=0.06,volume=4dB,alimiter=limit=0.91[out]',
    '-map', '[out]', '-ar', '48000', '-c:a', 'pcm_s24le', "$previewDir/toss_jp_reel_mix.wav"
)

# Delivery preview.
Invoke-FFmpeg @(
    '-y', '-i', "$previewDir/toss_jp_reel_text_lock.mp4", '-i', "$previewDir/toss_jp_reel_mix.wav",
    '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
    '-t', '12.8', '-movflags', '+faststart', '-metadata', 'title=TOSS Card Japan Tourist Reel v01',
    "$previewDir/TOSS_JP_reel_v01.mp4"
)

Write-Output "Built $previewDir/TOSS_JP_reel_v01.mp4"
