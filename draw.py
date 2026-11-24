"""Draw the 24 November 2026 world-news front page (1024x1024 PNG).

Stories as reported on Tuesday 24 November 2026: Russian warplanes
enter South Korea's air defence zone near Ulleung Island and a mistaken
alert sends islanders to shelter; states sue Musk firms over sexualised
images made by the Grok chatbot; Rep. Jimmy Gomez resigns after a House
Ethics finding; the inside story of Trump's push to restore Jensen Huang
at Nvidia; Moscow warns Kyiv after the Libya and Baltic attacks.
Layout is a newspaper front page: masthead with the date, one lead
story, four stories in a grid, and a short 'also' strip.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
BLACK = (20, 20, 20)
RED = (176, 0, 0)
BLUE = (24, 78, 140)
GREEN = (0, 110, 60)
GREY = (90, 90, 90)
LIGHT = (238, 240, 244)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit width in pixels, word by word."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, width, fill, spacing=4):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def panel(draw, box, label, headline, body, icon, accent):
    """One story panel: coloured label bar, headline, body, small icon."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], outline=BLACK, width=2)
    draw.rectangle([x0, y0, x1, y0 + 26], fill=accent)
    draw.text((x0 + 10, y0 + 4), label, font=font(SANS_B, 15), fill=WHITE)
    icon(draw, x1 - 118, y0 + 36, 104, 78)
    y = draw_wrapped(draw, (x0 + 12, y0 + 36), headline,
                     font(SANS_B, 24), x1 - x0 - 142, BLACK, spacing=2)
    draw_wrapped(draw, (x0 + 12, y + 4), body,
                 font(SANS, 17), x1 - x0 - 142, BLACK, spacing=3)


def icon_jet(draw, x, y, w, h):
    # A jet seen from above, nose up.
    draw.polygon([(x + 52, y + 2), (x + 62, y + 34), (x + 52, y + 76), (x + 42, y + 34)], fill=BLUE)
    draw.polygon([(x + 44, y + 30), (x + 6, y + 58), (x + 44, y + 52)], fill=BLUE)
    draw.polygon([(x + 60, y + 30), (x + 98, y + 58), (x + 60, y + 52)], fill=BLUE)
    draw.polygon([(x + 46, y + 62), (x + 58, y + 62), (x + 52, y + 78)], fill=BLUE)
    draw.ellipse([x + 48, y + 22, x + 56, y + 34], fill=WHITE)
    draw.arc([x + 8, y + 62, x + 96, y + 96], 200, 340, fill=GREY, width=2)


def icon_phone(draw, x, y, w, h):
    draw.rounded_rectangle([x + 28, y + 4, x + 76, y + 74], radius=8, fill=BLACK)
    draw.rectangle([x + 34, y + 12, x + 70, y + 58], fill=(60, 140, 220))
    draw.text((x + 42, y + 24), "AI", font=font(SANS_B, 24), fill=WHITE)
    draw.rectangle([x + 44, y + 64, x + 60, y + 68], fill=GREY)
    draw.line([x + 8, y + 20, x + 24, y + 20], fill=RED, width=4)
    draw.line([x + 8, y + 40, x + 24, y + 40], fill=RED, width=4)
    draw.line([x + 80, y + 20, x + 96, y + 20], fill=RED, width=4)
    draw.line([x + 80, y + 40, x + 96, y + 40], fill=RED, width=4)


def icon_dome(draw, x, y, w, h):
    # A capitol dome on a base.
    draw.rectangle([x + 8, y + 58, x + 96, y + 76], fill=(120, 120, 120))
    draw.rectangle([x + 16, y + 48, x + 88, y + 58], fill=(150, 150, 150))
    draw.pieslice([x + 22, y + 6, x + 82, y + 52], 180, 360, fill=BLUE)
    draw.rectangle([x + 48, y + 2, x + 56, y + 12], fill=BLUE)
    for cx in (28, 44, 60, 76):
        draw.rectangle([cx, y + 62, cx + 8, y + 72], fill=WHITE)


def icon_chip(draw, x, y, w, h):
    draw.rectangle([x + 24, y + 18, x + 80, y + 60], fill=BLACK)
    draw.rectangle([x + 34, y + 28, x + 70, y + 50], fill=(0, 180, 90))
    for px in (30, 46, 62):
        draw.line([x + px, y + 18, x + px, y + 6], fill=BLACK, width=3)
        draw.line([x + px, y + 60, x + px, y + 72], fill=BLACK, width=3)
    for py in (26, 42):
        draw.line([x + 24, y + py, x + 12, y + py], fill=BLACK, width=3)
        draw.line([x + 80, y + py, x + 92, y + py], fill=BLACK, width=3)


def icon_warning(draw, x, y, w, h):
    draw.polygon([(x + 52, y + 4), (x + 98, y + 72), (x + 6, y + 72)], fill=(255, 180, 0), outline=BLACK, width=2)
    draw.text((x + 44, y + 26), "!", font=font(SANS_B, 34), fill=BLACK)


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    d.rectangle([MARGIN - 6, MARGIN - 6, W - MARGIN + 6, H - MARGIN + 6], outline=BLACK, width=4)
    # Masthead
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 62)
    d.text(((W - d.textlength(title, font=tf)) / 2, 34), title, font=tf, fill=BLACK)
    d.line([MARGIN + 10, 118, W - MARGIN - 10, 118], fill=BLACK, width=3)
    dateline = "TUESDAY, 24 NOVEMBER 2026  •  WORLD NEWS IN ONE IMAGE"
    df = font(SANS_B, 22)
    d.text(((W - d.textlength(dateline, font=df)) / 2, 128), dateline, font=df, fill=RED)
    d.line([MARGIN + 10, 162, W - MARGIN - 10, 162], fill=BLACK, width=2)

    # Lead story: Korea air scare
    x0, y0, x1, y1 = MARGIN + 10, 176, W - MARGIN - 10, 400
    d.rectangle([x0, y0, x1, y1], outline=BLACK, width=2)
    d.rectangle([x0, y0, x1, y0 + 28], fill=RED)
    d.text((x0 + 12, y0 + 5), "KOREA  •  AIR DEFENCE ZONE", font=font(SANS_B, 16), fill=WHITE)
    icon_jet(d, x1 - 230, y0 + 42, 170, 170)
    y = draw_wrapped(d, (x0 + 14, y0 + 42), "RUSSIAN JETS SPARK\nKOREA AIR SCARE",
                     font(SANS_B, 46), 620, BLACK, spacing=2)
    draw_wrapped(d, (x0 + 14, y + 8),
                 "Russian warplanes enter South Korea's air defence zone near Ulleung Island; jets scramble, islanders shelter after a mistaken alert blames North Korea.",
                 font(SANS, 20), 620, BLACK, spacing=4)

    # Four stories in a 2x2 grid
    gx0, gy0 = MARGIN + 10, 416
    gw, gh, gap = (W - 2 * MARGIN - 20 - 16) // 2, 208, 14
    stories = [
        ("TECH  •  AI", "STATES SUE MUSK OVER GROK IMAGES", "Musk firms face lawsuits over a flood of sexualised images made by the AI chatbot Grok, saying it generated them on demand.", icon_phone, RED),
        ("US POLITICS", "GOMEZ QUITS AFTER ETHICS FINDING", "Democratic Rep. Jimmy Gomez resigns after the House Ethics panel finds substantial evidence of sexual misconduct with a staffer.", icon_dome, BLUE),
        ("TECH  •  MARKETS", "INSIDE TRUMP'S NVIDIA PUSH", "Vance lobbied the board over the weekend and Trump called it directly to bring Jensen Huang back as CEO, 11 days after he quit.", icon_chip, GREEN),
        ("RUSSIA-UKRAINE", "MOSCOW WARNS KYIV AFTER LIBYA STRIKES", "Russia warns of a dangerous trend after Ukraine's attacks in Libya and the Baltic; Moscow claims hits on drone sites in Sumy.", icon_warning, (90, 90, 90)),
    ]
    for i, (label, head, body, icon, accent) in enumerate(stories):
        x = gx0 + (i % 2) * (gw + gap)
        yy = gy0 + (i // 2) * (gh + gap)
        panel(d, (x, yy, x + gw, yy + gh), label, head, body, icon, accent)

    # Also strip
    ax0, ay0 = MARGIN + 10, gy0 + 2 * gh + gap + 8
    d.rectangle([ax0, ay0, W - MARGIN - 10, ay0 + 88], outline=BLACK, width=2)
    d.text((ax0 + 12, ay0 + 8), "ALSO ON 24 NOVEMBER", font=font(SANS_B, 16), fill=RED)
    draw_wrapped(d, (ax0 + 12, ay0 + 34),
                 "Pakistan quake, magnitude 4.1  •  China sentences an official to death for spying  •  German school bomb threats  •  Denmark to ban school phones  •  UN chief wants AI rules",
                 font(SANS, 18), W - 2 * MARGIN - 44, BLACK, spacing=4)
    d.text((MARGIN + 10, H - MARGIN - 14), "Stories as reported on 24 November 2026.",
           font=font(SANS, 14), fill=GREY)
    d.text((W - MARGIN - 10 - d.textlength("THE WORLD TODAY", font=font(SANS_B, 14)), H - MARGIN - 14),
           "THE WORLD TODAY", font=font(SANS_B, 14), fill=GREY)
    img.save("/home/hatch/workspace/makefun-news-image-24/entry/entry.png", "PNG", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
