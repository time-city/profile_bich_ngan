import sys
from PIL import Image

def process_image(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    pixels = img.load()
    
    width, height = img.size
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # If the pixel is not fully transparent
            if a > 0:
                # Check if it's black or dark grey
                # We consider it dark grey if R,G,B are all < 120 and the difference is small
                if r < 120 and g < 120 and b < 120 and max(r,g,b) - min(r,g,b) < 30:
                    # Invert the dark pixel to white, preserving its alpha
                    # Actually, to make gradients look natural, we could map 0->255 and 120->255.
                    # But pure white (255,255,255) is usually best for logos on dark backgrounds.
                    # Let's just make it pure white but keep the alpha.
                    pixels[x, y] = (255, 255, 255, a)
                # Let's also check the "Ben Thanh Tourist" text which might be a bit greenish?
                # Ben Thanh Tourist logo in screenshot looks dark grey.
                # "N A M A" is dark grey.
                # "SHILLA" is dark grey.
                # "HUAWEI" is dark grey.
                # If there are any very dark colored pixels that we missed, maybe increase threshold.
                elif r < 60 and g < 60 and b < 60:
                     pixels[x, y] = (255, 255, 255, a)
                    
    img.save(output_path, "WEBP")
    print(f"Saved {output_path}")

if __name__ == "__main__":
    process_image("asset/partner/partners.webp", "asset/partner/partners_white.webp")
