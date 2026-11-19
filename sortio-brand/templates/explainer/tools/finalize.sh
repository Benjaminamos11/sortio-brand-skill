#!/usr/bin/env bash
# Finish a rendered video for posting: loudness to -14 LUFS integrated / -1.5 dBTP (two-pass loudnorm, the level
# Instagram, TikTok and YouTube play at), optional poster frame baked in as frame 0, cover JPG, faststart.
#
# usage: bash tools/finalize.sh renders/explainer.mp4 [poster_seconds]
#   -> renders/explainer-final.mp4 (+ renders/explainer-cover.jpg when poster_seconds is given)
set -euo pipefail
in="$1"; poster="${2:-}"
base="${in%.mp4}"; out="$base-final.mp4"; tmp="$base-tmp.mp4"
command -v ffmpeg >/dev/null || { echo "ffmpeg is not installed (see references/tools-setup.md)"; exit 1; }

vcodec=(-c:v copy)
if [ -n "$poster" ]; then
  ffmpeg -v error -y -ss "$poster" -i "$in" -frames:v 1 -q:v 2 "$base-cover.jpg"
  # replace frame 0 with the poster, so every feed thumbnail shows a settled frame (duration and sync stay the same)
  ffmpeg -v error -y -i "$in" -i "$base-cover.jpg" -filter_complex "[0:v][1:v]overlay=enable='eq(n\,0)'[v]" \
    -map "[v]" -map 0:a -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a copy "$tmp"
  in="$tmp"
fi

json=$(ffmpeg -hide_banner -i "$in" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
get() { echo "$json" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
ln="loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(get input_i):measured_TP=$(get input_tp):measured_LRA=$(get input_lra):measured_thresh=$(get input_thresh):offset=$(get target_offset):linear=true"
ffmpeg -v error -y -i "$in" -map 0:v -map 0:a "${vcodec[@]}" -af "$ln,aresample=48000" -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$out"
rm -f "$tmp"

I=$(ffmpeg -hide_banner -nostats -i "$out" -af ebur128=peak=true -f null - 2>&1 | awk '/Summary/{s=1} s&&/ I:/{print $2}')
TP=$(ffmpeg -hide_banner -nostats -i "$out" -af ebur128=peak=true -f null - 2>&1 | awk '/Summary/{s=1} s&&/Peak:/{p=$2} END{print p}')
info=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate:format=duration,size -of default=nw=1:nk=1 "$out" | tr '\n' ' ')
echo "$out: $info| $I LUFS integrated, true peak $TP dBFS"
[ -n "$poster" ] && echo "cover: $base-cover.jpg"
