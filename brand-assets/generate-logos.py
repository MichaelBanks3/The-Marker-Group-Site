"""
The Marker Group brand asset generator.

Creates:
  - Primary wordmarks
  - Stacked logos
  - Icon variants
  - Favicon and Apple touch icon
  - Open Graph image
  - Social profile image
  - Email signature lockup
  - Brand palette reference sheet
"""

from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont


SCRIPT_DIR = Path(__file__).resolve().parent
FONT_DIR = SCRIPT_DIR / "fonts"
LOGO_DIR = SCRIPT_DIR / "logos"
SITE_IMAGE_DIR = SCRIPT_DIR.parent / "images"

LORA = str(FONT_DIR / "Lora-Regular.ttf")
LORA_ITALIC = str(FONT_DIR / "Lora-Italic.ttf")
POPPINS_LIGHT = str(FONT_DIR / "Poppins-Light.ttf")
POPPINS_REGULAR = str(FONT_DIR / "Poppins-Regular.ttf")
POPPINS_MEDIUM = str(FONT_DIR / "Poppins-Medium.ttf")
POPPINS_SEMIBOLD = str(FONT_DIR / "Poppins-SemiBold.ttf")

NAVY = (11, 29, 53)
NAVY_MID = (19, 43, 77)
NAVY_LIGHT = (26, 58, 92)
WHITE = (255, 255, 255)
COPPER = (193, 154, 107)
COPPER_LIGHT = (212, 180, 142)
COPPER_DARK = (166, 124, 82)
OFF_WHITE = (245, 243, 238)
WARM_GRAY = (242, 240, 235)
TEXT_DARK = (28, 28, 28)
TEXT_BODY = (61, 61, 61)
TEXT_MUTED = (107, 114, 128)

SCALE = 4


def s(value):
    return int(value * SCALE)


def ensure_dirs():
    LOGO_DIR.mkdir(parents=True, exist_ok=True)
    SITE_IMAGE_DIR.mkdir(parents=True, exist_ok=True)


def save_image(image, filename, save_to_site=False):
    image.save(LOGO_DIR / filename, "PNG", dpi=(300, 300))
    if save_to_site:
        image.save(SITE_IMAGE_DIR / filename, "PNG", dpi=(300, 300))
    print(f"  {filename}: {image.size[0]}x{image.size[1]}px")


def load_font(path, size):
    return ImageFont.truetype(path, size)


def draw_thick_line(draw, x1, y1, x2, y2, thickness, color):
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx * dx + dy * dy)
    if length == 0:
        return

    px = -dy / length * thickness / 2
    py = dx / length * thickness / 2
    draw.polygon(
        [
            (x1 + px, y1 + py),
            (x1 - px, y1 - py),
            (x2 - px, y2 - py),
            (x2 + px, y2 + py),
        ],
        fill=color,
    )


def draw_monogram(draw, cx, cy, size, fg_color, accent_color):
    stroke = max(size // 12, 2)
    monogram_width = int(size * 0.82)
    monogram_height = int(size * 0.68)

    left = cx - monogram_width // 2
    right = cx + monogram_width // 2
    top = cy - monogram_height // 2
    bottom = cy + monogram_height // 2
    center_y = top + monogram_height * 0.45

    draw_thick_line(draw, left, bottom, left, top + stroke, stroke, fg_color)
    draw_thick_line(draw, left, top + stroke, cx, center_y, stroke, fg_color)
    draw_thick_line(draw, cx, center_y, right, top + stroke, stroke, fg_color)
    draw_thick_line(draw, right, top + stroke, right, bottom, stroke, fg_color)

    bar_width = int(monogram_width * 0.35)
    bar_height = max(stroke // 2, 2)
    bar_y = bottom + int(size * 0.1)
    draw.rounded_rectangle(
        [cx - bar_width // 2, bar_y, cx + bar_width // 2, bar_y + bar_height],
        radius=max(bar_height // 2, 1),
        fill=accent_color,
    )


def draw_wordmark(draw, x, y, fg_color, muted_color, serif_font, sans_font):
    draw.text((x, y), "THE", fill=muted_color, font=sans_font)
    the_bbox = draw.textbbox((x, y), "THE", font=sans_font)
    marker_y = the_bbox[3] + s(4)
    draw.text((x, marker_y), "MARKER", fill=fg_color, font=serif_font)
    marker_bbox = draw.textbbox((x, marker_y), "MARKER", font=serif_font)
    group_y = marker_bbox[3] + s(2)
    draw.text((x, group_y), "GROUP", fill=muted_color, font=sans_font)
    return draw.textbbox((x, y), "THE", font=sans_font), marker_bbox, draw.textbbox((x, group_y), "GROUP", font=sans_font)


def make_full_logo(bg_color, fg_color, muted_color, accent_color, filename, transparent=False):
    serif_font = load_font(LORA, s(50))
    sans_font = load_font(POPPINS_MEDIUM, s(17))
    mark_size = s(64)
    gap = s(30)
    pad_x = s(46)
    pad_y = s(34)

    temp = Image.new("RGBA", (s(1000), s(400)), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp)
    wordmark_bbox = temp_draw.multiline_textbbox(
        (0, 0), "THE\nMARKER\nGROUP", font=sans_font, spacing=s(8)
    )
    marker_bbox = temp_draw.textbbox((0, 0), "MARKER", font=serif_font)
    wordmark_width = max(wordmark_bbox[2] - wordmark_bbox[0], marker_bbox[2] - marker_bbox[0])
    wordmark_height = s(118)

    width = pad_x * 2 + mark_size + gap + wordmark_width
    height = pad_y * 2 + max(mark_size, wordmark_height)
    background = (0, 0, 0, 0) if transparent else bg_color
    image = Image.new("RGBA", (width, height), background)
    draw = ImageDraw.Draw(image)

    mark_cx = pad_x + mark_size // 2
    mark_cy = height // 2 - s(6)
    draw_monogram(draw, mark_cx, mark_cy, mark_size, fg_color, accent_color)

    wordmark_x = pad_x + mark_size + gap
    wordmark_y = pad_y
    draw.text((wordmark_x, wordmark_y), "THE", fill=muted_color, font=sans_font)
    draw.text((wordmark_x, wordmark_y + s(22)), "MARKER", fill=fg_color, font=serif_font)
    draw.text((wordmark_x, wordmark_y + s(76)), "GROUP", fill=muted_color, font=sans_font)

    save_image(image, filename, save_to_site=True)


def make_stacked_logo(bg_color, fg_color, muted_color, accent_color, filename):
    serif_font = load_font(LORA, s(42))
    sans_font = load_font(POPPINS_MEDIUM, s(15))
    mark_size = s(72)
    pad = s(50)

    temp = Image.new("RGBA", (s(600), s(500)), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp)
    marker_bbox = temp_draw.textbbox((0, 0), "MARKER", font=serif_font)
    group_bbox = temp_draw.textbbox((0, 0), "GROUP", font=sans_font)

    width = max(mark_size, marker_bbox[2], group_bbox[2]) + pad * 2
    height = pad * 2 + mark_size + s(72)
    image = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    cx = width // 2
    draw_monogram(draw, cx, pad + mark_size // 2, mark_size, fg_color, accent_color)
    draw.text((cx - temp_draw.textbbox((0, 0), "THE", font=sans_font)[2] // 2, pad + mark_size + s(8)), "THE", fill=muted_color, font=sans_font)
    draw.text((cx - marker_bbox[2] // 2, pad + mark_size + s(26)), "MARKER", fill=fg_color, font=serif_font)
    draw.text((cx - group_bbox[2] // 2, pad + mark_size + s(74)), "GROUP", fill=muted_color, font=sans_font)

    save_image(image, filename)


def make_icon(filename, background, fg_color, accent_color, size=512, transparent=False):
    bg = (0, 0, 0, 0) if transparent else background
    image = Image.new("RGBA", (size, size), bg)
    draw = ImageDraw.Draw(image)
    draw_monogram(draw, size // 2, size // 2 - int(size * 0.03), int(size * 0.5), fg_color, accent_color)
    save_image(image, filename)


def make_favicons():
    for size in (32, 64, 180):
        image = Image.new("RGBA", (size, size), NAVY)
        draw = ImageDraw.Draw(image)
        draw_monogram(draw, size // 2, size // 2 - 1, int(size * 0.66), WHITE, COPPER)

        if size == 32:
            save_image(image, "favicon.png", save_to_site=True)
        elif size == 180:
            save_image(image, "apple-touch-icon.png")
        else:
            save_image(image, f"favicon-{size}.png")


def make_social_profile():
    size = 400
    image = Image.new("RGBA", (size, size), NAVY)
    draw = ImageDraw.Draw(image)
    draw_monogram(draw, size // 2, size // 2 - 8, int(size * 0.48), WHITE, COPPER)
    save_image(image, "social-profile.png")


def make_email_signature():
    serif_font = load_font(LORA, 28)
    width, height = 360, 72
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    draw_monogram(draw, 28, height // 2 - 2, 34, NAVY, COPPER)
    text_bbox = draw.textbbox((0, 0), "THE MARKER GROUP", font=serif_font)
    text_y = (height - (text_bbox[3] - text_bbox[1])) // 2 - text_bbox[1]
    draw.text((58, text_y), "THE MARKER GROUP", fill=NAVY, font=serif_font)
    save_image(image, "email-signature.png")


def make_og_image():
    width, height = 1200, 630
    image = Image.new("RGBA", (width, height), NAVY)
    draw = ImageDraw.Draw(image)

    serif_font = load_font(LORA, 56)
    italic_font = load_font(LORA_ITALIC, 56)
    sans_font = load_font(POPPINS_REGULAR, 22)

    draw.rounded_rectangle([56, 56, width - 56, height - 56], radius=24, outline=(*COPPER, 80), width=2)
    draw_monogram(draw, width // 2, 180, 104, WHITE, COPPER)

    title = "THE MARKER GROUP"
    title_bbox = draw.textbbox((0, 0), title, font=serif_font)
    draw.text(((width - (title_bbox[2] - title_bbox[0])) // 2, 260), title, fill=WHITE, font=serif_font)

    line_one = "Higher Education GTM"
    line_two = "Consulting with depth."
    one_bbox = draw.textbbox((0, 0), line_one, font=sans_font)
    two_bbox = draw.textbbox((0, 0), line_two, font=italic_font)
    draw.text(((width - (one_bbox[2] - one_bbox[0])) // 2, 352), line_one, fill=COPPER_LIGHT, font=sans_font)
    draw.text(((width - (two_bbox[2] - two_bbox[0])) // 2, 390), line_two, fill=WHITE, font=italic_font)

    save_image(image, "og-image.png", save_to_site=True)


def make_brand_palette():
    width, height = 1600, 1000
    image = Image.new("RGBA", (width, height), OFF_WHITE)
    draw = ImageDraw.Draw(image)

    title_font = load_font(LORA, 62)
    heading_font = load_font(POPPINS_SEMIBOLD, 22)
    body_font = load_font(POPPINS_REGULAR, 18)
    sample_font = load_font(LORA, 38)

    draw.text((90, 74), "The Marker Group", fill=NAVY, font=title_font)
    draw.text((92, 150), "Brand palette and typography reference", fill=TEXT_MUTED, font=body_font)

    swatches = [
        ("Navy", "#0B1D35", NAVY),
        ("Navy Mid", "#132B4D", NAVY_MID),
        ("Navy Light", "#1A3A5C", NAVY_LIGHT),
        ("Copper", "#C19A6B", COPPER),
        ("Copper Light", "#D4B48E", COPPER_LIGHT),
        ("Copper Dark", "#A67C52", COPPER_DARK),
        ("Off-White", "#F5F3EE", OFF_WHITE),
        ("Warm Gray", "#F2F0EB", WARM_GRAY),
    ]

    start_x = 90
    start_y = 230
    box_w = 320
    box_h = 140
    gap_x = 30
    gap_y = 26

    for index, (label, hex_value, color) in enumerate(swatches):
        row = index // 4
        col = index % 4
        x = start_x + col * (box_w + gap_x)
        y = start_y + row * (box_h + gap_y)
        draw.rounded_rectangle([x, y, x + box_w, y + box_h], radius=18, fill=color)
        text_color = WHITE if sum(color) < 500 else NAVY
        draw.text((x + 22, y + 26), label, fill=text_color, font=heading_font)
        draw.text((x + 22, y + 74), hex_value, fill=text_color, font=body_font)

    draw.text((90, 590), "Typography", fill=NAVY, font=heading_font)
    draw.text((90, 632), "Lora brings editorial authority to headings and lockups.", fill=TEXT_BODY, font=body_font)
    draw.text((90, 680), "The Marker Group", fill=NAVY, font=sample_font)
    draw.text((90, 758), "Poppins keeps interfaces and copy clean, readable, and modern.", fill=TEXT_BODY, font=body_font)
    draw.text((90, 804), "Higher education GTM consulting for serious operators.", fill=NAVY_MID, font=load_font(POPPINS_MEDIUM, 28))

    save_image(image, "brand-palette.png")


def main():
    ensure_dirs()
    print("Generating brand assets...\n")

    print("Primary logos:")
    make_full_logo(NAVY, WHITE, (255, 255, 255, 170), COPPER, "marker-group-logo-dark.png")
    make_full_logo(WHITE, NAVY, (*NAVY, 145), COPPER, "marker-group-logo-light.png")
    make_full_logo(None, WHITE, (255, 255, 255, 170), COPPER, "marker-group-logo-transparent.png", transparent=True)

    print("\nStacked logos:")
    make_stacked_logo(NAVY, WHITE, (255, 255, 255, 170), COPPER, "marker-group-stacked-dark.png")
    make_stacked_logo(WHITE, NAVY, (*NAVY, 145), COPPER, "marker-group-stacked-light.png")

    print("\nIcons:")
    make_icon("icon-navy.png", NAVY, WHITE, COPPER)
    make_icon("icon-white.png", WHITE, NAVY, COPPER)
    make_icon("icon-transparent.png", NAVY, WHITE, COPPER, transparent=True)

    print("\nPlatform assets:")
    make_favicons()
    make_social_profile()
    make_email_signature()
    make_og_image()
    make_brand_palette()

    print("\nDone.")


if __name__ == "__main__":
    main()
