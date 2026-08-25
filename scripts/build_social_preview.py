#!/usr/bin/env python3
"""Build the repository and website social preview from deterministic primitives."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
WIDTH = 1280
HEIGHT = 640

INK = "#0D1718"
WHITE = "#FBF9F3"
CORAL = "#F16F51"
CYAN = "#4BCBD5"
MUTED = "#9BA9AA"


def font(candidates: list[str], size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size, index=index)
            except OSError:
                continue
    return ImageFont.load_default(size=size)


SERIF = [
    "/System/Library/Fonts/NewYork.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]
SANS = [
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
MONO = [
    "/System/Library/Fonts/Menlo.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
]


def build() -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), INK)
    draw = ImageDraw.Draw(image)

    for x in range(0, WIDTH, 40):
        draw.line((x, 0, x, HEIGHT), fill="#142122", width=1)
    for y in range(0, HEIGHT, 40):
        draw.line((0, y, WIDTH, y), fill="#142122", width=1)

    draw.rectangle((0, 0, 18, HEIGHT), fill=CORAL)
    draw.rectangle((18, 0, 27, HEIGHT), fill=CYAN)
    draw.rectangle((905, -80, 1370, 190), fill="#112728")
    draw.ellipse((1010, -118, 1390, 262), outline=CYAN, width=2)
    draw.ellipse((1080, -48, 1320, 192), outline=CORAL, width=2)

    brand_font = font(MONO, 24)
    draw.text((76, 58), ">_", font=brand_font, fill=CORAL)
    draw.text((126, 58), "AGENT PAPERS", font=brand_font, fill=WHITE)
    draw.text((1035, 61), "2026 / EVIDENCE", font=font(MONO, 16), fill=CYAN)

    headline = font(SERIF, 82)
    headline_italic = font(
        [
            "/System/Library/Fonts/NewYorkItalic.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
        ],
        82,
    )
    draw.text((74, 148), "Claude Code & Codex", font=headline, fill=WHITE)
    draw.text((74, 236), "research, with receipts.", font=headline_italic, fill=CORAL)

    draw.text(
        (78, 360),
        "Exact models  /  methods  /  results  /  comparison limits",
        font=font(SANS, 24),
        fill=MUTED,
    )

    draw.line((78, 425, 1202, 425), fill="#314041", width=1)
    metrics = [
        ("18,269", "OFFICIAL RECORDS"),
        ("13", "PRODUCT-LEVEL PAPERS"),
        ("19", "SHAREABLE EVIDENCE PAGES"),
    ]
    starts = [78, 360, 670]
    for (value, label), x in zip(metrics, starts, strict=True):
        draw.text((x, 460), value, font=font(SERIF, 50), fill=CYAN)
        draw.text((x, 529), label, font=font(MONO, 13), fill=MUTED)

    draw.text(
        (777, 594),
        "micromilo.github.io/awesome-claude-code-codex-papers",
        font=font(MONO, 12),
        fill=WHITE,
    )
    return image


def main() -> None:
    image = build()
    outputs = [ROOT / "website" / "public" / "og.png", ROOT / "assets" / "social-preview.png"]
    for output in outputs:
        output.parent.mkdir(parents=True, exist_ok=True)
        image.save(output, format="PNG", optimize=True, compress_level=9)


if __name__ == "__main__":
    main()
