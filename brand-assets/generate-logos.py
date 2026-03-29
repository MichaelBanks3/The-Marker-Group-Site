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
RESAMPLE = Image.Resampling.LANCZOS if hasattr(Image, "Resampling") else Image.LANCZOS


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


def rgba(color, alpha):
    return (*color[:3], alpha)


def mix(color_a, color_b, amount):
    return tuple(int(color_a[index] * (1 - amount) + color_b[index] * amount) for index in range(3))


def measure_text(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def get_wordmark_metrics(serif_font, sans_font, variant):
    temp = Image.new("RGBA", (s(800), s(400)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(temp)
    if variant == "stacked":
        positions = {"THE": 0, "MARKER": s(26), "GROUP": s(86)}
    else:
        positions = {"THE": 0, "MARKER": s(22), "GROUP": s(84)}

    the_bbox = draw.textbbox((0, positions["THE"]), "THE", font=sans_font)
    marker_bbox = draw.textbbox((0, positions["MARKER"]), "MARKER", font=serif_font)
    group_bbox = draw.textbbox((0, positions["GROUP"]), "GROUP", font=sans_font)

    the_width = the_bbox[2] - the_bbox[0]
    marker_width = marker_bbox[2] - marker_bbox[0]
    group_width = group_bbox[2] - group_bbox[0]

    top = min(the_bbox[1], marker_bbox[1], group_bbox[1])
    bottom = max(the_bbox[3], marker_bbox[3], group_bbox[3])
    return {
        "the_width": the_width,
        "marker_width": marker_width,
        "group_width": group_width,
        "width": max(the_width, marker_width, group_width),
        "height": bottom - top,
        "top": top,
        "positions": positions,
    }


def draw_wordmark(draw, x, y, fg_color, muted_color, serif_font, sans_font, variant="full", centered=False):
    metrics = get_wordmark_metrics(serif_font, sans_font, variant)
    base_y = y - metrics["top"]

    if centered:
        the_x = x + (metrics["width"] - metrics["the_width"]) // 2
        marker_x = x + (metrics["width"] - metrics["marker_width"]) // 2
        group_x = x + (metrics["width"] - metrics["group_width"]) // 2
    else:
        the_x = x
        marker_x = x
        group_x = x

    draw.text((the_x, base_y + metrics["positions"]["THE"]), "THE", fill=muted_color, font=sans_font)
    draw.text((marker_x, base_y + metrics["positions"]["MARKER"]), "MARKER", fill=fg_color, font=serif_font)
    draw.text((group_x, base_y + metrics["positions"]["GROUP"]), "GROUP", fill=muted_color, font=sans_font)

    return metrics


def draw_flag_mark(draw, left, top, width, height, pole_color, flag_color, cup_color):
    pole_x = left + int(width * 0.24)
    pole_top = top + int(height * 0.08)
    pole_bottom = top + int(height * 0.84)
    pole_width = max(int(width * 0.06), 2)

    draw.rounded_rectangle(
        [pole_x - pole_width // 2, pole_top, pole_x + pole_width // 2, pole_bottom],
        radius=max(pole_width // 2, 1),
        fill=pole_color,
    )

    flag_top = top + int(height * 0.14)
    flag_height = int(height * 0.24)
    flag_length = int(width * 0.62)
    flag_x = pole_x + pole_width // 2
    flag_points = [
        (flag_x, flag_top),
        (flag_x + int(flag_length * 0.34), flag_top - int(flag_height * 0.04)),
        (flag_x + int(flag_length * 0.86), flag_top + int(flag_height * 0.18)),
        (flag_x + flag_length, flag_top + int(flag_height * 0.42)),
        (flag_x + int(flag_length * 0.74), flag_top + int(flag_height * 0.76)),
        (flag_x + int(flag_length * 0.28), flag_top + int(flag_height * 0.64)),
        (flag_x, flag_top + flag_height),
    ]
    draw.polygon(flag_points, fill=flag_color)

    if width >= 56:
        highlight_points = [
            (flag_x + int(flag_length * 0.08), flag_top + int(flag_height * 0.12)),
            (flag_x + int(flag_length * 0.38), flag_top + int(flag_height * 0.04)),
            (flag_x + int(flag_length * 0.72), flag_top + int(flag_height * 0.19)),
            (flag_x + int(flag_length * 0.49), flag_top + int(flag_height * 0.34)),
            (flag_x + int(flag_length * 0.18), flag_top + int(flag_height * 0.28)),
        ]
        draw.polygon(highlight_points, fill=rgba(mix(flag_color[:3], WHITE, 0.38), 170))

    cup_center_x = pole_x
    cup_center_y = top + int(height * 0.92)
    cup_radius = max(int(width * 0.07), 3)
    inner_radius = max(cup_radius // 2, 2)
    outline_width = max(pole_width // 2, 1)

    draw.ellipse(
        [
            cup_center_x - cup_radius,
            cup_center_y - cup_radius,
            cup_center_x + cup_radius,
            cup_center_y + cup_radius,
        ],
        outline=cup_color,
        width=outline_width,
    )
    draw.ellipse(
        [
            cup_center_x - inner_radius,
            cup_center_y - inner_radius,
            cup_center_x + inner_radius,
            cup_center_y + inner_radius,
        ],
        fill=pole_color,
    )


def make_mark_tile(size, background, pole_color, flag_color, cup_color, transparent=False):
    upscale = 4 if size <= 180 else 2
    render_size = size * upscale
    bg_color = (0, 0, 0, 0) if transparent else background
    image = Image.new("RGBA", (render_size, render_size), bg_color)
    draw = ImageDraw.Draw(image)

    mark_width = int(render_size * 0.5)
    mark_height = int(render_size * 0.8)
    left = (render_size - mark_width) // 2 - int(render_size * 0.01)
    top = (render_size - mark_height) // 2
    draw_flag_mark(draw, left, top, mark_width, mark_height, pole_color, flag_color, cup_color)

    if upscale > 1:
        image = image.resize((size, size), RESAMPLE)

    return image


def make_full_logo(bg_color, fg_color, muted_color, accent_color, filename, transparent=False):
    serif_font = load_font(LORA, s(50))
    sans_font = load_font(POPPINS_MEDIUM, s(17))
    metrics = get_wordmark_metrics(serif_font, sans_font, "full")
    mark_width = s(64)
    mark_height = s(98)
    gap = s(24)
    pad_x = s(46)
    pad_y = s(30)

    width = pad_x * 2 + mark_width + gap + metrics["width"]
    height = pad_y * 2 + max(mark_height, metrics["height"])
    background = (0, 0, 0, 0) if transparent else bg_color
    image = Image.new("RGBA", (width, height), background)
    draw = ImageDraw.Draw(image)

    mark_left = pad_x
    mark_top = (height - mark_height) // 2
    draw_flag_mark(draw, mark_left, mark_top, mark_width, mark_height, fg_color, accent_color, accent_color)

    wordmark_x = pad_x + mark_width + gap
    wordmark_y = (height - metrics["height"]) // 2
    draw_wordmark(
        draw,
        wordmark_x,
        wordmark_y,
        fg_color,
        muted_color,
        serif_font,
        sans_font,
        variant="full",
        centered=True,
    )

    save_image(image, filename, save_to_site=True)


def make_stacked_logo(bg_color, fg_color, muted_color, accent_color, filename):
    serif_font = load_font(LORA, s(42))
    sans_font = load_font(POPPINS_MEDIUM, s(15))
    metrics = get_wordmark_metrics(serif_font, sans_font, "stacked")
    mark_width = s(76)
    mark_height = s(112)
    gap = s(20)
    pad = s(50)

    width = max(mark_width, metrics["width"]) + pad * 2
    height = pad * 2 + mark_height + gap + metrics["height"]
    image = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    mark_left = (width - mark_width) // 2
    draw_flag_mark(draw, mark_left, pad, mark_width, mark_height, fg_color, accent_color, accent_color)
    draw_wordmark(
        draw,
        (width - metrics["width"]) // 2,
        pad + mark_height + gap,
        fg_color,
        muted_color,
        serif_font,
        sans_font,
        variant="stacked",
        centered=True,
    )

    save_image(image, filename)


def make_icon(filename, background, fg_color, accent_color, size=512, transparent=False):
    image = make_mark_tile(size, background, fg_color, accent_color, accent_color, transparent=transparent)
    save_image(image, filename)


def make_favicons():
    for size in (32, 64, 180):
        image = make_mark_tile(size, NAVY, WHITE, COPPER, COPPER)

        if size == 32:
            save_image(image, "favicon.png", save_to_site=True)
        elif size == 180:
            save_image(image, "apple-touch-icon.png")
        else:
            save_image(image, f"favicon-{size}.png")


def make_social_profile():
    size = 400
    image = make_mark_tile(size, NAVY, WHITE, COPPER, COPPER)
    save_image(image, "social-profile.png")


def make_email_signature():
    serif_font = load_font(LORA, 28)
    width, height = 390, 78
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    draw_flag_mark(draw, 12, 9, 36, 60, NAVY, COPPER, COPPER)
    text_bbox = draw.textbbox((0, 0), "THE MARKER GROUP", font=serif_font)
    text_y = (height - (text_bbox[3] - text_bbox[1])) // 2 - text_bbox[1]
    draw.text((64, text_y), "THE MARKER GROUP", fill=NAVY, font=serif_font)
    save_image(image, "email-signature.png")


def make_og_image():
    width, height = 1200, 630
    image = Image.new("RGBA", (width, height), NAVY)
    draw = ImageDraw.Draw(image)

    serif_font = load_font(LORA, 56)
    italic_font = load_font(LORA_ITALIC, 56)
    sans_font = load_font(POPPINS_REGULAR, 22)

    draw.rounded_rectangle([56, 56, width - 56, height - 56], radius=24, outline=(*COPPER, 80), width=2)
    draw_flag_mark(draw, width // 2 - 42, 86, 84, 150, WHITE, COPPER, COPPER_LIGHT)

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
    draw_flag_mark(draw, width - 220, 62, 88, 146, NAVY, COPPER, COPPER_DARK)

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
