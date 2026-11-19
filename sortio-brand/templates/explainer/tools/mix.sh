#!/usr/bin/env bash
# Mix the explainer audio: voice (vo/voice.wav) plus an optional music bed that ducks under the voice, two-pass
# loudness to -14 LUFS integrated / -1.5 dBTP, written to audio/mix.m4a (the file index.html plays).
#
# usage: bash tools/mix.sh                      voice only
#        bash tools/mix.sh audio/music.mp3      voice + music bed (looped or cut to length, -20 dB, ducked, faded)
# The length is the data-duration that tools/build_subtitles.py wrote on #root in index.html (voice + end card).
set -euo pipefail
music="${1:-}"; voice=vo/voice.wav; out=audio/mix.m4a
command -v ffmpeg >/dev/null || { echo "ffmpeg is not installed (see references/tools-setup.md)"; exit 1; }
[ -f "$voice" ] || { echo "no $voice yet: run tools/vo_elevenlabs.py first"; exit 1; }
T=$(python3 -c "import re;print(re.search(r'<div id=\"root\"[^>]*?data-duration=\"([\d.]+)\"', open('index.html').read()).group(1))")
mkdir -p audio; tmp=audio/.premix.wav

if [ -n "$music" ]; then
  ffmpeg -v error -y -i "$voice" -stream_loop -1 -i "$music" -filter_complex \
    "[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,asplit=2[v1][v2];\
     [1:a]aresample=48000,atrim=0:$T,volume=-20dB,afade=t=in:st=0:d=1.5,afade=t=out:st=$(python3 -c "print(max(0,$T-2.5))"):d=2.5[m];\
     [v1]apad=whole_dur=$T[sc];[m][sc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=450[duck];\
     [v2]apad=whole_dur=$T[v];[v][duck]amix=inputs=2:duration=first:normalize=0[out]" \
    -map "[out]" -t "$T" -c:a pcm_s24le "$tmp"
else
  ffmpeg -v error -y -i "$voice" -af "aresample=48000,pan=stereo|c0=c0|c1=c0,apad=whole_dur=$T" -t "$T" -c:a pcm_s24le "$tmp"
fi

json=$(ffmpeg -hide_banner -i "$tmp" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
get() { echo "$json" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
if [ "$(get input_i)" = "-inf" ]; then
  echo "the voice is silent (draft voice?): writing silence"; ffmpeg -v error -y -i "$tmp" -c:a aac -b:a 128k "$out"
else
  ln="loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true"
  ffmpeg -v error -y -i "$tmp" -af "$ln,aresample=48000" -c:a aac -b:a 192k -ar 48000 "$out"
fi
rm -f "$tmp"
echo "wrote $out ($T s)"
