#!/usr/bin/env python3
"""The Passport Page of a Country That Isn't There.

Renders one uncaptioned open passport spread for the Maritime Sovereignty
of Cinnabar Reach -- a sulfur-mining, water-rationed archipelago that does
not exist -- and writes it to /output/entry.png.

Left page: data page (portrait, personal data, MRZ with real ICAO check
digits, SPECIMEN overprint). Right page: visa/stamp page with four
consistent stamps (all after the 12 MAR 2024 issue date) and the telling
paperwork detail: a Class-3 desalination-tax stamp rationing the holder's
own drinking water to 3.5 litres a day.

No network. Only Pillow + the bundled portrait are needed.
"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/output/entry.png"

W, H = 1024, 724
PAGE_W, PAGE_H = 472, 652
PAGE_Y = 36
LEFT_X = 28
RIGHT_X = 524

PAPER = (244, 239, 226)
PAPER_DARK = (232, 226, 208)
INK = (28, 32, 38)
INK_SOFT = (74, 78, 84)
RULE = (150, 140, 118)
GOLD = (146, 110, 42)
TEAL = (18, 92, 96)
DESK = (38, 34, 30)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- MRZ ----
def _val(ch):
    if ch.isdigit():
        return int(ch)
    if ch == "<":
        return 0
    return ord(ch) - 55  # A=10 ... Z=35


def check_digit(s):
    total = 0
    for i, ch in enumerate(s):
        total += _val(ch) * (7, 3, 1)[i % 3]
    return str(total % 10)


def mrz_lines():
    # Holder: VANCE, LINNEA. DOB 14 OCT 1981. Issue 12 MAR 2024, exp 11 MAR 2034.
    line1 = "P<CRBVANCE<<LINNEA"
    line1 = line1 + "<" * (44 - len(line1))
    doc = "CR2024084"
    d1 = check_digit(doc)
    dob = "811014"
    d2 = check_digit(dob)
    exp = "340311"
    d3 = check_digit(exp)
    personal = "<" * 14
    d4 = check_digit(personal)
    body = doc + d1 + "CRB" + dob + d2 + "F" + exp + d3 + personal + d4
    d5 = check_digit(body)
    return line1, body + d5


# ------------------------------------------------------------- helpers ----
def guilloche(draw, x0, y0, x1, y1, color, step=7, amp=2.2):
    """Fine wavy security lines across a rectangle."""
    for yy in range(y0, y1, step):
        pts = []
        for xx in range(x0, x1 + 1, 8):
            pts.append((xx, yy + amp * math.sin((xx - x0) / 26.0 + yy / 40.0)))
        draw.line(pts, fill=color, width=1)


def stamp_layer(size, draw_fn, angle):
    """A transparent layer with one stamp drawn on it, rotated."""
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    draw_fn(d, size)
    return layer.rotate(angle, resample=Image.BICUBIC, expand=False)


def stamp_text(d, cx, cy, lines, color, sizes, spacing=3):
    """Centered stacked lines of text inside a stamp."""
    y = cy - sum(sizes) // 2 - spacing * (len(lines) - 1) // 2
    for text, sz in zip(lines, sizes):
        f = font(SANS_B, sz)
        w = d.textlength(text, font=f)
        d.text((cx - w / 2, y), text, font=f, fill=color)
        y += sz + spacing


# ------------------------------------------------------------ data page ---
def draw_data_page(base):
    page = Image.new("RGBA", (PAGE_W, PAGE_H), PAPER + (255,))
    d = ImageDraw.Draw(page)
    guilloche(d, 14, 96, PAGE_W - 14, PAGE_H - 92, (216, 207, 186))

    # frame
    d.rectangle([10, 10, PAGE_W - 11, PAGE_H - 11], outline=RULE, width=2)
    d.rectangle([14, 14, PAGE_W - 15, PAGE_H - 15], outline=RULE, width=1)

    # --- coat of arms: circle, crossed picks, droplet -------------------
    cx, cy, r = 52, 52, 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=2)
    d.ellipse([cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4], outline=GOLD, width=1)
    d.line([cx - 13, cy + 12, cx + 13, cy - 12], fill=GOLD, width=3)
    d.line([cx - 13, cy - 12, cx + 13, cy + 12], fill=GOLD, width=3)
    d.ellipse([cx - 5, cy - 2, cx + 5, cy + 10], fill=TEAL)
    d.polygon([(cx, cy - 12), (cx - 5, cy - 2), (cx + 5, cy - 2)], fill=TEAL)

    # --- header ----------------------------------------------------------
    d.text((86, 30), "MARITIME SOVEREIGNTY", font=font(SERIF_B, 17), fill=INK)
    d.text((86, 50), "OF CINNABAR REACH", font=font(SERIF_B, 17), fill=INK)
    d.text((86, 71), "KEDAULATAN MARITIM CINNABAR REACH", font=font(SANS, 8), fill=INK_SOFT)
    d.line([86, 86, PAGE_W - 26, 86], fill=RULE, width=1)
    d.text((86, 92), "PASSPORT  ·  PASPOR", font=font(SERIF_B, 13), fill=TEAL)
    d.text((330, 94), "No. CR 2024 08417", font=font(SANS_B, 10), fill=INK)

    # --- portrait --------------------------------------------------------
    px, py, pw, ph = 30, 122, 158, 208
    d.rectangle([px - 4, py - 4, px + pw + 4, py + ph + 4], fill=(255, 255, 255), outline=RULE, width=1)
    portrait = Image.open(os.path.join(HERE, "assets", "portrait.png")).convert("RGB")
    portrait = portrait.resize((pw, ph), Image.LANCZOS)
    page.paste(portrait, (px, py))
    d.text((px, py + ph + 8), "HOLDER'S PHOTOGRAPH", font=font(SANS, 7), fill=INK_SOFT)

    # --- personal data ---------------------------------------------------
    fields = [
        ("SURNAME / NAMA KELUARGA", "VANCE"),
        ("GIVEN NAMES / NAMA", "LINNEA"),
        ("NATIONALITY / KEWARGANEGARAAN", "CINNABARI"),
        ("DATE OF BIRTH / TGL LAHIR", "14 OCT 1981"),
        ("PLACE OF BIRTH / TEMPAT LAHIR", "PORT-VERMILION"),
        ("SEX / JENIS KELAMIN", "F"),
        ("OCCUPATION / PEKERJAAN", "CHIEF SURVEYOR"),
        ("DATE OF ISSUE / TGL TERBIT", "12 MAR 2024"),
        ("DATE OF EXPIRY / BERLAKU S.D.", "11 MAR 2034"),
        ("AUTHORITY / OTORITAS", "GUILD OF SURVEYORS"),
    ]
    fx, fy = 210, 122
    y = fy
    for label, value in fields:
        d.text((fx, y), label, font=font(SANS, 7), fill=INK_SOFT)
        d.text((fx, y + 10), value, font=font(SERIF_B, 13), fill=INK)
        y += 30
    # signature line
    d.line([fx, y + 2, fx + 150, y + 2], fill=INK_SOFT, width=1)
    d.text((fx, y + 6), "HOLDER'S SIGNATURE", font=font(SANS, 7), fill=INK_SOFT)
    sig = ImageDraw.Draw(page)
    sig.line([(fx + 8, y - 2), (fx + 30, y - 12), (fx + 52, y - 3), (fx + 74, y - 11),
              (fx + 96, y - 4), (fx + 118, y - 10), (fx + 140, y - 5)],
             fill=(40, 48, 70), width=2)

    # --- languages column ------------------------------------------------
    ly = 470
    d.line([30, ly, PAGE_W - 30, ly], fill=RULE, width=1)
    d.text((30, ly + 8), "LANGUAGES / BAHASA:  CINNABARI  ·  ENGLISH",
           font=font(SANS_B, 9), fill=INK)
    d.text((30, ly + 24), "This passport is the property of the Guild of Surveyors of",
           font=font(SANS, 8), fill=INK_SOFT)
    d.text((30, ly + 35), "Cinnabar Reach. Loss must be reported at once to the nearest",
           font=font(SANS, 8), fill=INK_SOFT)
    d.text((30, ly + 46), "Guild checkpoint. Finder: return to Port-Vermilion, Dock 3.",
           font=font(SANS, 8), fill=INK_SOFT)

    # --- MRZ -------------------------------------------------------------
    my = PAGE_H - 78
    d.rectangle([20, my - 8, PAGE_W - 20, my + 44], fill=(233, 228, 212))
    l1, l2 = mrz_lines()
    mf = font(MONO_B, 15)
    d.text((30, my), l1, font=mf, fill=INK)
    d.text((30, my + 20), l2, font=mf, fill=INK)

    # --- SPECIMEN overprint ----------------------------------------------
    over = Image.new("RGBA", (PAGE_W, PAGE_H), (0, 0, 0, 0))
    od = ImageDraw.Draw(over)
    of = font(SANS_B, 40)
    od.text((40, 360), "SPECIMEN", font=of, fill=(178, 34, 34, 38))
    over = over.rotate(-24, resample=Image.BICUBIC, center=(PAGE_W // 2, PAGE_H // 2))
    page.alpha_composite(over)

    base.alpha_composite(page, (LEFT_X, PAGE_Y))


# ------------------------------------------------------------ stamp page --
def draw_stamp_page(base):
    page = Image.new("RGBA", (PAGE_W, PAGE_H), PAPER + (255,))
    d = ImageDraw.Draw(page)
    guilloche(d, 14, 60, PAGE_W - 14, PAGE_H - 14, (216, 207, 186))

    d.rectangle([10, 10, PAGE_W - 11, PAGE_H - 11], outline=RULE, width=2)
    d.rectangle([14, 14, PAGE_W - 15, PAGE_H - 15], outline=RULE, width=1)

    d.text((30, 28), "VISAS", font=font(SERIF_B, 18), fill=INK)
    d.text((120, 32), "VISA  ·  HALAMAN VISA", font=font(SANS, 9), fill=INK_SOFT)
    d.text((PAGE_W - 66, 32), "PAGE 12", font=font(SANS_B, 9), fill=INK_SOFT)
    d.line([30, 56, PAGE_W - 30, 56], fill=RULE, width=1)

    PURPLE = (104, 52, 148, 210)
    RUST = (166, 58, 32, 210)
    TEAL_I = (14, 110, 112, 210)
    NAVY = (34, 58, 120, 210)

    def hex_stamp(dd, size):
        cx, cy = size[0] // 2, size[1] // 2
        pts = []
        for k in range(6):
            a = math.pi / 3 * k - math.pi / 6
            pts.append((cx + 108 * math.cos(a), cy + 62 * math.sin(a)))
        dd.polygon(pts, outline=PURPLE, width=3)
        pts2 = []
        for k in range(6):
            a = math.pi / 3 * k - math.pi / 6
            pts2.append((cx + 98 * math.cos(a), cy + 54 * math.sin(a)))
        dd.polygon(pts2, outline=PURPLE, width=1)
        stamp_text(dd, cx, cy - 4,
                   ["SULTANATE OF", "QAL-HADAR", "ARRIVAL", "19 APR 2024", "SILT-PORT 04"],
                   PURPLE, [9, 13, 10, 12, 8])

    def circle_stamp(dd, size):
        cx, cy = size[0] // 2, size[1] // 2
        dd.ellipse([cx - 78, cy - 62, cx + 78, cy + 62], outline=RUST, width=3)
        dd.ellipse([cx - 70, cy - 54, cx + 70, cy + 54], outline=RUST, width=1)
        stamp_text(dd, cx, cy - 4,
                   ["ISLE OF BRINE-HEAD", "DEPARTURE", "03 JUN 2024", "CUSTOMS GATE 9"],
                   RUST, [9, 13, 12, 8])

    def oval_stamp(dd, size):
        cx, cy = size[0] // 2, size[1] // 2
        dd.ellipse([cx - 104, cy - 56, cx + 104, cy + 56], outline=TEAL_I, width=3)
        dd.ellipse([cx - 94, cy - 48, cx + 94, cy + 48], outline=TEAL_I, width=1)
        stamp_text(dd, cx, cy - 4,
                   ["HIGH BASALT REPUBLIC", "ARRIVAL", "14 NOV 2024", "SKY-DOCK ALPHA"],
                   TEAL_I, [9, 13, 12, 8])

    def rect_stamp(dd, size):
        cx, cy = size[0] // 2, size[1] // 2
        dd.rectangle([cx - 106, cy - 52, cx + 106, cy + 52], outline=NAVY, width=3)
        dd.rectangle([cx - 98, cy - 44, cx + 98, cy + 44], outline=NAVY, width=1)
        stamp_text(dd, cx, cy - 4,
                   ["PORT-VERMILION — HOME", "ARRIVAL", "02 DEC 2024", "GUILD CHECKPOINT 2"],
                   NAVY, [9, 13, 12, 8])

    stamps = [
        (hex_stamp, (236, 130), (30, 70), -4),
        (circle_stamp, (200, 130), (252, 75), 5),
        (oval_stamp, (236, 130), (30, 268), -6),
        (rect_stamp, (236, 130), (252, 273), 3),
    ]
    for fn, size, pos, angle in stamps:
        layer = stamp_layer(size, fn, angle)
        page.alpha_composite(layer, pos)

    # --- the telling detail: desalination-tax stamp ----------------------
    tax = Image.new("RGBA", (430, 92), (0, 0, 0, 0))
    td = ImageDraw.Draw(tax)
    td.rectangle([2, 2, 427, 89], outline=(196, 148, 0, 235), width=3)
    td.rectangle([7, 7, 422, 84], outline=(196, 148, 0, 235), width=1)
    td.text((16, 10), "CLASS-3 DESALINATION TAX — PAID",
            font=font(SANS_B, 13), fill=(168, 124, 0, 255))
    td.text((16, 30), "HOLDER ALLOTTED 3.5 L / DAY ATMOSPHERIC",
            font=font(SANS_B, 11), fill=(168, 124, 0, 255))
    td.text((16, 48), "FRESHWATER RATION  ·  GUILD TARIFF 7-C",
            font=font(SANS_B, 11), fill=(168, 124, 0, 255))
    td.text((16, 68), "UNAUTHORISED AIR-CONDENSATION: ASSET SEIZURE",
            font=font(SANS, 9), fill=(168, 124, 0, 255))
    tax = tax.rotate(-3, resample=Image.BICUBIC, expand=True)
    page.alpha_composite(tax, (22, 505))

    # --- visa condition box ----------------------------------------------
    d.rectangle([30, 420, 240, 478], outline=INK_SOFT, width=1)
    d.text((38, 426), "CONDITION OF ENTRY", font=font(SANS_B, 8), fill=INK)
    d.text((38, 438), "Holder must present water-", font=font(SANS, 8), fill=INK_SOFT)
    d.text((38, 449), "ration card at all Guild", font=font(SANS, 8), fill=INK_SOFT)
    d.text((38, 460), "checkpoints.", font=font(SANS, 8), fill=INK_SOFT)

    base.alpha_composite(page, (RIGHT_X, PAGE_Y))


def main():
    random.seed(20261121)
    img = Image.new("RGBA", (W, H), DESK + (255,))
    # desk shading + page shadows
    d = ImageDraw.Draw(img)
    for i in range(60):
        d.rectangle([0, H - 60 + i, W, H - 59 + i], fill=(30 + i // 4, 27 + i // 4, 24 + i // 4))
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rectangle([LEFT_X + 6, PAGE_Y + 8, LEFT_X + PAGE_W + 6, PAGE_Y + PAGE_H + 8],
                 fill=(0, 0, 0, 90))
    sd.rectangle([RIGHT_X + 6, PAGE_Y + 8, RIGHT_X + PAGE_W + 6, PAGE_Y + PAGE_H + 8],
                 fill=(0, 0, 0, 90))
    shadow = shadow.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(6))
    img.alpha_composite(shadow)

    draw_data_page(img)
    draw_stamp_page(img)

    # centre gutter shadow
    gutter = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gutter)
    for x in range(506, 522):
        a = 70 - abs(x - 514) * 8
        gd.line([(x, PAGE_Y), (x, PAGE_Y + PAGE_H)], fill=(0, 0, 0, max(a, 0)), width=1)
    img.alpha_composite(gutter)

    out = img.convert("RGB")
    try:
        os.makedirs("/output", exist_ok=True)
        out.save(OUT, "PNG", optimize=True)
    except OSError:
        os.makedirs("output", exist_ok=True)
        out.save("output/entry.png", "PNG", optimize=True)
    print("wrote", OUT, out.size)


if __name__ == "__main__":
    main()
