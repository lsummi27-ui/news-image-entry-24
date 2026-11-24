"""Render the front page for Tuesday 24 November 2026 as a 1024x1024 PNG.

The page is a newspaper front page for THE WORLD TODAY. Its stories are
the ones reported on 24 November 2026: Russian jets trigger an air scare
off South Korea, US states sue Musk's firms over sexualised Grok images,
Rep. Jimmy Gomez quits after an ethics finding, the inside story of the
push to bring Jensen Huang back to Nvidia, and Moscow warning Kyiv after
the Libya strikes. A short strip at the foot carries the remaining items.

Everything is drawn with Pillow: one lead story across the top, four
stories in a two-by-two grid underneath, and the "also" strip at the
bottom. The drawing constants below (text, fonts, sizes, colours and
positions) are the page itself, so they must not be changed casually.
"""

from PIL import Image, ImageDraw, ImageFont

# Page geometry and palette.
PAGE_W, PAGE_H = 1024, 1024
EDGE = 28
INK = (20, 20, 20)
CRIMSON = (176, 0, 0)
NAVY = (24, 78, 140)
EMERALD = (0, 110, 60)
ASH = (90, 90, 90)
PALE = (238, 240, 244)
PAPER = (255, 255, 255)

# DejaVu faces used throughout the page.
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load_font(path, size):
    """Load one TrueType face at the requested point size."""
    return ImageFont.truetype(path, size)


def fit_lines(pen, text, fnt, width):
    """Split text into lines that each fit inside width pixels.

    Wrapping is greedy and word by word; explicit newlines in the text
    start a fresh paragraph.
    """
    out = []
    for para in text.split("\n"):
        words = para.split()
        current = ""
        for word in words:
            trial = (current + " " + word).strip()
            if pen.textlength(trial, font=fnt) <= width:
                current = trial
            else:
                if current:
                    out.append(current)
                current = word
        if current:
            out.append(current)
    return out


def paint_lines(pen, xy, text, fnt, width, fill, spacing=4):
    """Draw wrapped text starting at xy; return the y below the last line."""
    x, y = xy
    for line in fit_lines(pen, text, fnt, width):
        pen.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def sketch_plane(pen, x, y, w, h):
    """A jet seen from above, nose pointing up, with a faint vapour arc."""
    pen.polygon([(x + 52, y + 2), (x + 62, y + 34), (x + 52, y + 76), (x + 42, y + 34)], fill=NAVY)
    pen.polygon([(x + 44, y + 30), (x + 6, y + 58), (x + 44, y + 52)], fill=NAVY)
    pen.polygon([(x + 60, y + 30), (x + 98, y + 58), (x + 60, y + 52)], fill=NAVY)
    pen.polygon([(x + 46, y + 62), (x + 58, y + 62), (x + 52, y + 78)], fill=NAVY)
    pen.ellipse([x + 48, y + 22, x + 56, y + 34], fill=PAPER)
    pen.arc([x + 8, y + 62, x + 96, y + 96], 200, 340, fill=ASH, width=2)


def sketch_handset(pen, x, y, w, h):
    """A phone showing an AI screen, with red alert ticks on both sides."""
    pen.rounded_rectangle([x + 28, y + 4, x + 76, y + 74], radius=8, fill=INK)
    pen.rectangle([x + 34, y + 12, x + 70, y + 58], fill=(60, 140, 220))
    pen.text((x + 42, y + 24), "AI", font=load_font(SANS_BOLD, 24), fill=PAPER)
    pen.rectangle([x + 44, y + 64, x + 60, y + 68], fill=ASH)
    pen.line([x + 8, y + 20, x + 24, y + 20], fill=CRIMSON, width=4)
    pen.line([x + 8, y + 40, x + 24, y + 40], fill=CRIMSON, width=4)
    pen.line([x + 80, y + 20, x + 96, y + 20], fill=CRIMSON, width=4)
    pen.line([x + 80, y + 40, x + 96, y + 40], fill=CRIMSON, width=4)


def sketch_capitol(pen, x, y, w, h):
    """A capitol dome standing on a stepped base."""
    pen.rectangle([x + 8, y + 58, x + 96, y + 76], fill=(120, 120, 120))
    pen.rectangle([x + 16, y + 48, x + 88, y + 58], fill=(150, 150, 150))
    pen.pieslice([x + 22, y + 6, x + 82, y + 52], 180, 360, fill=NAVY)
    pen.rectangle([x + 48, y + 2, x + 56, y + 12], fill=NAVY)
    for cx in (28, 44, 60, 76):
        pen.rectangle([cx, y + 62, cx + 8, y + 72], fill=PAPER)


def sketch_processor(pen, x, y, w, h):
    """A chip with pins on all four sides and a green core."""
    pen.rectangle([x + 24, y + 18, x + 80, y + 60], fill=INK)
    pen.rectangle([x + 34, y + 28, x + 70, y + 50], fill=(0, 180, 90))
    for px in (30, 46, 62):
        pen.line([x + px, y + 18, x + px, y + 6], fill=INK, width=3)
        pen.line([x + px, y + 60, x + px, y + 72], fill=INK, width=3)
    for py in (26, 42):
        pen.line([x + 24, y + py, x + 12, y + py], fill=INK, width=3)
        pen.line([x + 80, y + py, x + 92, y + py], fill=INK, width=3)


def sketch_alert(pen, x, y, w, h):
    """A yellow warning triangle with an exclamation mark."""
    pen.polygon([(x + 52, y + 4), (x + 98, y + 72), (x + 6, y + 72)], fill=(255, 180, 0), outline=INK, width=2)
    pen.text((x + 44, y + 26), "!", font=load_font(SANS_BOLD, 34), fill=INK)


def story_box(pen, box, tag, head, body, glyph, accent):
    """One grid story: coloured tag bar, headline, body, small picture.

    The picture sits at the top right; the text column keeps clear of it.
    """
    left, top, right, bottom = box
    pen.rectangle([left, top, right, bottom], outline=INK, width=2)
    pen.rectangle([left, top, right, top + 26], fill=accent)
    pen.text((left + 10, top + 4), tag, font=load_font(SANS_BOLD, 15), fill=PAPER)
    glyph(pen, right - 118, top + 36, 104, 78)
    cursor = paint_lines(
        pen, (left + 12, top + 36), head,
        load_font(SANS_BOLD, 24), right - left - 142, INK, spacing=2)
    paint_lines(
        pen, (left + 12, cursor + 4), body,
        load_font(SANS_REG, 17), right - left - 142, INK, spacing=3)


def build_page():
    """Draw the whole front page and save it next to this script."""
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    pen = ImageDraw.Draw(page)

    # Outer frame.
    pen.rectangle(
        [EDGE - 6, EDGE - 6, PAGE_W - EDGE + 6, PAGE_H - EDGE + 6],
        outline=INK, width=4)

    # Masthead: paper name, rule, dateline, rule.
    name = "THE WORLD TODAY"
    name_font = load_font(SERIF_BOLD, 62)
    pen.text(
        ((PAGE_W - pen.textlength(name, font=name_font)) / 2, 34),
        name, font=name_font, fill=INK)
    pen.line([EDGE + 10, 118, PAGE_W - EDGE - 10, 118], fill=INK, width=3)
    dateline = "TUESDAY, 24 NOVEMBER 2026  •  WORLD NEWS IN ONE IMAGE"
    date_font = load_font(SANS_BOLD, 22)
    pen.text(
        ((PAGE_W - pen.textlength(dateline, font=date_font)) / 2, 128),
        dateline, font=date_font, fill=CRIMSON)
    pen.line([EDGE + 10, 162, PAGE_W - EDGE - 10, 162], fill=INK, width=2)

    # Lead story: the Korea air scare, full width.
    lx0, ly0, lx1, ly1 = EDGE + 10, 176, PAGE_W - EDGE - 10, 400
    pen.rectangle([lx0, ly0, lx1, ly1], outline=INK, width=2)
    pen.rectangle([lx0, ly0, lx1, ly0 + 28], fill=CRIMSON)
    pen.text(
        (lx0 + 12, ly0 + 5), "KOREA  •  AIR DEFENCE ZONE",
        font=load_font(SANS_BOLD, 16), fill=PAPER)
    sketch_plane(pen, lx1 - 230, ly0 + 42, 170, 170)
    after_head = paint_lines(
        pen, (lx0 + 14, ly0 + 42), "RUSSIAN JETS SPARK\nKOREA AIR SCARE",
        load_font(SANS_BOLD, 46), 620, INK, spacing=2)
    paint_lines(
        pen, (lx0 + 14, after_head + 8),
        "Russian warplanes enter South Korea's air defence zone near Ulleung Island; jets scramble, islanders shelter after a mistaken alert blames North Korea.",
        load_font(SANS_REG, 20), 620, INK, spacing=4)

    # Four stories in a two-by-two grid.
    grid_x, grid_y = EDGE + 10, 416
    cell_w, cell_h, cell_gap = (PAGE_W - 2 * EDGE - 20 - 16) // 2, 208, 14
    items = [
        ("TECH  •  AI",
         "STATES SUE MUSK OVER GROK IMAGES",
         "Musk firms face lawsuits over a flood of sexualised images made by the AI chatbot Grok, saying it generated them on demand.",
         sketch_handset, CRIMSON),
        ("US POLITICS",
         "GOMEZ QUITS AFTER ETHICS FINDING",
         "Democratic Rep. Jimmy Gomez resigns after the House Ethics panel finds substantial evidence of sexual misconduct with a staffer.",
         sketch_capitol, NAVY),
        ("TECH  •  MARKETS",
         "INSIDE TRUMP'S NVIDIA PUSH",
         "Vance lobbied the board over the weekend and Trump called it directly to bring Jensen Huang back as CEO, 11 days after he quit.",
         sketch_processor, EMERALD),
        ("RUSSIA-UKRAINE",
         "MOSCOW WARNS KYIV AFTER LIBYA STRIKES",
         "Russia warns of a dangerous trend after Ukraine's attacks in Libya and the Baltic; Moscow claims hits on drone sites in Sumy.",
         sketch_alert, (90, 90, 90)),
    ]
    for pos, (tag, head, body, glyph, accent) in enumerate(items):
        # Two columns: even positions on the left, odd on the right.
        cx = grid_x + (pos % 2) * (cell_w + cell_gap)
        cy = grid_y + (pos // 2) * (cell_h + cell_gap)
        story_box(pen, (cx, cy, cx + cell_w, cy + cell_h), tag, head, body, glyph, accent)

    # Also strip: the remaining items of the day.
    strip_x, strip_y = EDGE + 10, grid_y + 2 * cell_h + cell_gap + 8
    pen.rectangle(
        [strip_x, strip_y, PAGE_W - EDGE - 10, strip_y + 88],
        outline=INK, width=2)
    pen.text(
        (strip_x + 12, strip_y + 8), "ALSO ON 24 NOVEMBER",
        font=load_font(SANS_BOLD, 16), fill=CRIMSON)
    paint_lines(
        pen, (strip_x + 12, strip_y + 34),
        "Pakistan quake, magnitude 4.1  •  China sentences an official to death for spying  •  German school bomb threats  •  Denmark to ban school phones  •  UN chief wants AI rules",
        load_font(SANS_REG, 18), PAGE_W - 2 * EDGE - 44, INK, spacing=4)

    # Footer: source note on the left, paper name on the right.
    pen.text(
        (EDGE + 10, PAGE_H - EDGE - 14),
        "Stories as reported on 24 November 2026.",
        font=load_font(SANS_REG, 14), fill=ASH)
    pen.text(
        (PAGE_W - EDGE - 10 - pen.textlength("THE WORLD TODAY", font=load_font(SANS_BOLD, 14)),
         PAGE_H - EDGE - 14),
        "THE WORLD TODAY", font=load_font(SANS_BOLD, 14), fill=ASH)

    page.save("/home/hatch/workspace/makefun-news-image-24/entry/entry.png", "PNG", optimize=True)
    print("saved entry.png", page.size)


if __name__ == "__main__":
    build_page()
