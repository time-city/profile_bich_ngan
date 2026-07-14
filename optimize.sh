#!/bin/bash

# Optimize Images
echo "Optimizing Images..."
find asset -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | while read -r img; do
  WIDTH=$(sips -g pixelWidth "$img" | grep pixelWidth | awk '{print $2}')
  HEIGHT=$(sips -g pixelHeight "$img" | grep pixelHeight | awk '{print $2}')
  
  if [ -n "$WIDTH" ] && [ -n "$HEIGHT" ]; then
    if [ "$WIDTH" -gt 1920 ] || [ "$HEIGHT" -gt 1920 ]; then
      echo "Resizing $img (${WIDTH}x${HEIGHT} -> max 1920)"
      sips -Z 1920 "$img" > /dev/null
    fi
  fi
done

# Optimize Videos
echo "Optimizing Videos..."
find asset -type f -iname "*.mp4" | while read -r vid; do
  echo "Optimizing video: $vid"
  # Scale to max 1280 width (720p equivalent), CRF 28 for good web compression
  /opt/homebrew/bin/ffmpeg -y -i "$vid" -vf "scale='min(1280,iw)':-2" -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 128k "${vid}.tmp.mp4" </dev/null
  if [ $? -eq 0 ]; then
    mv "${vid}.tmp.mp4" "$vid"
  else
    echo "Error optimizing $vid. Removing tmp file."
    rm -f "${vid}.tmp.mp4"
  fi
done

echo "Optimization complete!"
