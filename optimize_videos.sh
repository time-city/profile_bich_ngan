#!/bin/bash
# Optimize Videos
echo "Optimizing Videos..."
find asset -type f \( -iname "*.mp4" -o -iname "*.mov" \) | while read -r vid; do
  echo "Optimizing video: $vid"
  # Scale to max 1280 width (720p equivalent), CRF 28 for good web compression
  /opt/homebrew/bin/ffmpeg -y -i "$vid" -vf "scale='min(1280,iw)':-2" -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 128k "${vid}.tmp.mp4" </dev/null
  if [ $? -eq 0 ]; then
    # Optional: check if the new file is actually smaller before replacing
    old_size=$(wc -c < "$vid")
    new_size=$(wc -c < "${vid}.tmp.mp4")
    if [ "$new_size" -lt "$old_size" ]; then
      mv "${vid}.tmp.mp4" "$vid"
      echo "Optimized $vid successfully."
    else
      echo "Optimization didn't reduce size for $vid. Keeping original."
      rm -f "${vid}.tmp.mp4"
    fi
  else
    echo "Error optimizing $vid. Removing tmp file."
    rm -f "${vid}.tmp.mp4"
  fi
done

echo "Video Optimization complete!"
