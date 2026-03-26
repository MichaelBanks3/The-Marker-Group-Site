"""
The Marker Group — Logo Generator (Concept 3: The Flag Pin)
============================================================
Navy: #0F1F3D  |  Fonts: Lora (serif), Poppins (sans)

Generates 3 PNG versions: dark, light, transparent
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ── BRAND COLORS ──────────────────────────────────────────
NAVY = (15, 31, 61)        # #0F1F3D
WHITE = (255, 255, 255)

# ── RENDER SETTINGS ───────────────────────────────────────
SCALE = 4                  # multiplier for high-res output

# ── FONT PATHS (update these if running locally) ─────────
SERIF_PATH  = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"   # "Marker" - fallback serif
SANS_PATH   = "/System/Library/Fonts/Helvetica.ttc"  # "THE" & "GROUP" - fallback sans

# ── OUTPUT DIRECTORY ──────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "images")


def s(val):
    """Scale a value by the global multiplier."""
    return int(val * SCALE)


def get_visual_top_bottom(font, text, draw, y_origin=0):
    """
    Render text and return the actual visual top/bottom y-coordinates
    relative to y_origin. This accounts for font metrics properly
    so we can measure true optical whitespace between lines.
    """
    bbox = draw.textbbox((0, y_origin), text, font=font)
    return bbox[1], bbox[3]  # visual top, visual bottom


def make_logo(bg_color, fg_color, fg_muted_rgba, flag_fill_rgba, filename, transparent=False):

    # ── FONTS ─────────────────────────────────────────
    font_sub    = ImageFont.truetype(SANS_PATH,  s(48))   # THE & GROUP (increased size)
    font_marker = ImageFont.truetype(SERIF_PATH, s(95))   # Marker

    # ── MEASURE TEXT ──────────────────────────────────
    tmp = Image.new('RGBA', (s(800), s(400)))
    td  = ImageDraw.Draw(tmp)

    # Get widths
    the_w     = td.textbbox((0, 0), "THE",    font=font_sub)[2]
    marker_w  = td.textbbox((0, 0), "Marker", font=font_marker)[2]
    group_w   = td.textbbox((0, 0), "GROUP",  font=font_sub)[2]

    # To get truly equal OPTICAL gaps, we need to know where
    # each line's pixels actually start and end vertically.
    # We'll place lines at test positions, measure visual bounds,
    # then compute the layout so the whitespace is identical.

    # First, get each line's internal height (visual top to visual bottom)
    the_vtop,     the_vbot     = get_visual_top_bottom(font_sub,    "THE",    td)
    marker_vtop,  marker_vbot  = get_visual_top_bottom(font_marker, "Marker", td)
    group_vtop,   group_vbot   = get_visual_top_bottom(font_sub,    "GROUP",  td)

    the_vis_h     = the_vbot - the_vtop
    marker_vis_h  = marker_vbot - marker_vtop
    group_vis_h   = group_vbot - group_vtop

    # The optical gap we want between the bottom of one line's pixels
    # and the top of the next line's pixels
    OPTICAL_GAP = s(18)

    # Total visual height of the text block
    total_vis_h = the_vis_h + OPTICAL_GAP + marker_vis_h + OPTICAL_GAP + group_vis_h

    # ── PIN DIMENSIONS ────────────────────────────────
    flag_w, flag_h  = s(42), s(30)
    pin_gap         = s(90)         # space between pole and text (increased for wider logo)
    pin_area_w      = flag_w + s(6)

    content_w = pin_area_w + pin_gap + marker_w

    # ── CANVAS ────────────────────────────────────────
    pad_x = s(90)
    pad_y = s(40)
    dot_extra = s(22)

    W = content_w + pad_x * 2
    H = total_vis_h + pad_y * 2 + dot_extra

    if transparent:
        img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    else:
        img = Image.new('RGBA', (W, H), bg_color)
    draw = ImageDraw.Draw(img)

    # ── COMPUTE Y POSITIONS ───────────────────────────
    # We want visual tops/bottoms to be evenly spaced.
    # Start from pad_y as the visual top of "THE".
    #
    # For each line, the draw y-origin differs from the visual top
    # by an offset (the font's internal padding above the glyphs).

    text_left = pad_x + pin_area_w + pin_gap

    # Offsets: how far below the draw origin does the visual top start?
    the_offset    = the_vtop       # visual top when drawn at y=0
    marker_offset = marker_vtop
    group_offset  = group_vtop

    # Position Marker first (unchanged from original position)
    the_draw_y_original = pad_y - the_offset
    the_vis_bottom_original = pad_y + the_vis_h
    marker_vis_top = the_vis_bottom_original + OPTICAL_GAP
    marker_draw_y  = marker_vis_top - marker_offset
    marker_vis_bottom = marker_vis_top + marker_vis_h
    
    # Center THE between top padding and Marker top
    space_above_marker = marker_vis_top - pad_y
    the_vis_top = pad_y + (space_above_marker - the_vis_h) // 2
    the_draw_y = the_vis_top - the_offset

    # Visual top of GROUP = marker_vis_bottom + OPTICAL_GAP
    group_vis_top = marker_vis_bottom + OPTICAL_GAP
    group_draw_y  = group_vis_top - group_offset

    # ── DRAW TEXT ─────────────────────────────────────
    draw.text((text_left, the_draw_y),        "THE",    fill=fg_muted_rgba, font=font_sub)
    draw.text((text_left - s(3), marker_draw_y), "Marker", fill=fg_color,     font=font_marker)
    draw.text((text_left, group_draw_y),      "GROUP",  fill=fg_muted_rgba, font=font_sub)

    # ── FLAG PIN ──────────────────────────────────────
    pin_x      = pad_x + s(2)
    pin_top    = pad_y - s(10)
    pin_bottom = group_vis_top + group_vis_h + s(6)

    # Pole (rectangle for crisp rendering)
    pole_w = s(2)
    draw.rectangle(
        [pin_x - pole_w // 2, pin_top, pin_x + pole_w // 2, pin_bottom],
        fill=fg_color
    )

    # Flag pennant
    fx = pin_x + pole_w // 2 + s(1)
    flag_points = [
        (fx, pin_top),
        (fx + flag_w, pin_top + flag_h // 2),
        (fx, pin_top + flag_h)
    ]
    draw.polygon(flag_points, fill=flag_fill_rgba)

    # Marker dot at base of pole
    dot_cy = pin_bottom + s(14)
    r_out, r_in = s(6), s(2)
    draw.ellipse(
        [pin_x - r_out, dot_cy - r_out, pin_x + r_out, dot_cy + r_out],
        outline=fg_color, width=max(s(1), 3)
    )
    draw.ellipse(
        [pin_x - r_in, dot_cy - r_in, pin_x + r_in, dot_cy + r_in],
        fill=fg_color
    )

    # ── SAVE ──────────────────────────────────────────
    img.save(os.path.join(OUTPUT_DIR, filename), "PNG", dpi=(300, 300))
    print(f"  {filename}: {W}x{H}px  |  optical gap = {OPTICAL_GAP}px")


# ── GENERATE ALL VERSIONS ─────────────────────────────────
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generating logos...\n")

    make_logo(
        bg_color       = NAVY,
        fg_color       = WHITE,
        fg_muted_rgba  = (255, 255, 255, 160),
        flag_fill_rgba = (255, 255, 255, 255),
        filename       = "marker-group-logo-dark.png"
    )

    make_logo(
        bg_color       = WHITE,
        fg_color       = NAVY,
        fg_muted_rgba  = (15, 31, 61, 135),
        flag_fill_rgba = NAVY + (255,),
        filename       = "marker-group-logo-light.png"
    )

    make_logo(
        bg_color       = None,
        fg_color       = WHITE,
        fg_muted_rgba  = (255, 255, 255, 160),
        flag_fill_rgba = (255, 255, 255, 255),
        filename       = "marker-group-logo-transparent.png",
        transparent    = True
    )

    print("\nDone! All files saved to:", OUTPUT_DIR)
