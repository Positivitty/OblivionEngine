"""
Generate OblivionEngine app icons for all platforms.
Uses Catppuccin Mocha palette to match the app theme.

Generates:
  assets/icon.png     (1024x1024 master)
  assets/icon.ico     (Windows - multi-size)
  assets/iconset/      (macOS iconutil input)
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# Catppuccin Mocha palette (matching main.css)
BASE = "#1e1e2e"
MANTLE = "#181825"
CRUST = "#11111b"
SURFACE0 = "#313244"
SURFACE1 = "#45475a"
BLUE = "#89b4fa"
MAUVE = "#cba6f7"
TEXT = "#cdd6f4"
PEACH = "#fab387"

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def draw_rounded_rect(draw, bbox, radius, fill):
    x0, y0, x1, y1 = bbox
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.pieslice([x0, y0, x0 + 2*radius, y0 + 2*radius], 180, 270, fill=fill)
    draw.pieslice([x1 - 2*radius, y0, x1, y0 + 2*radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - 2*radius, x0 + 2*radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - 2*radius, y1 - 2*radius, x1, y1], 0, 90, fill=fill)

def create_icon(size=1024):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    margin = int(size * 0.06)
    radius = int(size * 0.18)

    # Outer rounded square - dark base
    draw_rounded_rect(draw, [margin, margin, size - margin, size - margin], radius, hex_to_rgb(CRUST))

    # Inner background with subtle gradient effect (draw horizontal bands)
    inner_margin = int(size * 0.08)
    inner_radius = int(size * 0.15)
    base_rgb = hex_to_rgb(BASE)
    mantle_rgb = hex_to_rgb(MANTLE)

    draw_rounded_rect(draw, [inner_margin, inner_margin, size - inner_margin, size - inner_margin], inner_radius, hex_to_rgb(BASE))

    # Draw a subtle top highlight band
    for y in range(inner_margin, inner_margin + int(size * 0.08)):
        t = (y - inner_margin) / (size * 0.08)
        color = lerp_color(hex_to_rgb(SURFACE0), base_rgb, t)
        alpha = int(60 * (1 - t))
        for x in range(inner_margin + inner_radius, size - inner_margin - inner_radius):
            img.putpixel((x, y), (*color, alpha))

    # === Terminal prompt symbol: > _ ===
    # Draw a stylized ">" chevron in blue->mauve gradient
    blue_rgb = hex_to_rgb(BLUE)
    mauve_rgb = hex_to_rgb(MAUVE)
    peach_rgb = hex_to_rgb(PEACH)

    cx, cy = size // 2, size // 2
    chevron_size = int(size * 0.28)
    stroke = int(size * 0.065)

    # Chevron ">" shape - left side, vertically centered
    chev_x = cx - int(size * 0.12)
    chev_y = cy - int(size * 0.04)

    # Draw chevron using thick lines
    # Top arm of >
    points_top = [
        (chev_x, chev_y - chevron_size // 2),
        (chev_x + chevron_size, chev_y),
    ]
    # Bottom arm of >
    points_bot = [
        (chev_x, chev_y + chevron_size // 2),
        (chev_x + chevron_size, chev_y),
    ]

    draw.line(points_top, fill=blue_rgb, width=stroke)
    draw.line(points_bot, fill=mauve_rgb, width=stroke)

    # Round the joints and endpoints
    for pt in [points_top[0], points_bot[0], (chev_x + chevron_size, chev_y)]:
        r = stroke // 2
        draw.ellipse([pt[0]-r, pt[1]-r, pt[0]+r, pt[1]+r], fill=mauve_rgb if pt == points_bot[0] else blue_rgb)

    # Center joint - blend color
    joint = (chev_x + chevron_size, chev_y)
    blend = lerp_color(blue_rgb, mauve_rgb, 0.5)
    r = stroke // 2 + 2
    draw.ellipse([joint[0]-r, joint[1]-r, joint[0]+r, joint[1]+r], fill=blend)

    # Cursor block (underscore / block cursor) to the right
    cursor_x = chev_x + chevron_size + int(size * 0.08)
    cursor_y = chev_y + chevron_size // 2 - stroke
    cursor_w = int(size * 0.12)
    cursor_h = stroke + 4

    # Blinking cursor block in peach
    draw_rounded_rect(draw, [cursor_x, cursor_y, cursor_x + cursor_w, cursor_y + cursor_h], 4, peach_rgb)

    # === Decorative dots in top-left (like terminal window buttons) ===
    dot_r = int(size * 0.018)
    dot_y_pos = margin + int(size * 0.08)
    dot_x_start = margin + int(size * 0.08)
    dot_spacing = int(size * 0.05)

    dot_colors = [hex_to_rgb("#f38ba8"), hex_to_rgb("#f9e2af"), hex_to_rgb("#a6e3a1")]  # red, yellow, green
    for i, color in enumerate(dot_colors):
        dx = dot_x_start + i * dot_spacing
        draw.ellipse([dx - dot_r, dot_y_pos - dot_r, dx + dot_r, dot_y_pos + dot_r], fill=color)

    # === Subtle "OE" text at bottom ===
    try:
        font_size = int(size * 0.08)
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", font_size)
    except (OSError, IOError):
        font = ImageFont.load_default()

    text = "OE"
    text_color = hex_to_rgb(SURFACE1)
    bbox_text = draw.textbbox((0, 0), text, font=font)
    tw = bbox_text[2] - bbox_text[0]
    th = bbox_text[3] - bbox_text[1]
    text_x = (size - tw) // 2 + int(size * 0.14)
    text_y = size - margin - int(size * 0.14)
    draw.text((text_x, text_y), text, fill=text_color, font=font)

    return img


def main():
    assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
    os.makedirs(assets_dir, exist_ok=True)

    print("Generating 1024x1024 master icon...")
    icon = create_icon(1024)
    master_path = os.path.join(assets_dir, "icon.png")
    icon.save(master_path, "PNG")
    print(f"  Saved: {master_path}")

    # Generate Windows .ico (multi-size)
    print("Generating Windows .ico...")
    ico_sizes = [16, 24, 32, 48, 64, 128, 256]
    ico_images = []
    for s in ico_sizes:
        resized = icon.resize((s, s), Image.LANCZOS)
        ico_images.append(resized)
    ico_path = os.path.join(assets_dir, "icon.ico")
    ico_images[0].save(ico_path, format="ICO", sizes=[(s, s) for s in ico_sizes], append_images=ico_images[1:])
    print(f"  Saved: {ico_path}")

    # Generate macOS .icns via iconutil
    print("Generating macOS .icns...")
    iconset_dir = os.path.join(assets_dir, "icon.iconset")
    os.makedirs(iconset_dir, exist_ok=True)

    icns_sizes = {
        "icon_16x16.png": 16,
        "icon_16x16@2x.png": 32,
        "icon_32x32.png": 32,
        "icon_32x32@2x.png": 64,
        "icon_128x128.png": 128,
        "icon_128x128@2x.png": 256,
        "icon_256x256.png": 256,
        "icon_256x256@2x.png": 512,
        "icon_512x512.png": 512,
        "icon_512x512@2x.png": 1024,
    }

    for name, s in icns_sizes.items():
        resized = icon.resize((s, s), Image.LANCZOS)
        resized.save(os.path.join(iconset_dir, name), "PNG")

    print(f"  Iconset created: {iconset_dir}")
    print("  Run: iconutil -c icns assets/icon.iconset -o assets/icon.icns")

    print("\nDone! Icons generated in assets/")


if __name__ == "__main__":
    main()
