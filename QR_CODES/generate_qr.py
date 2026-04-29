"""Generate QR codes for the EGU 2026 repository.

Run from this folder:
    python generate_qr.py

Outputs PNG (high resolution, for slides / print) and SVG (vector, for poster
printing) into the same folder.
"""

import qrcode
import qrcode.image.svg


REPO_URL = (
    "https://github.com/adityain2003/"
    "EGU-2026-Adding-reactive-transport-capabilities-to-the-2DSOIL-model-"
    "by-integrating-PhreeqcRM"
)

TARGETS = [
    {
        "name": "EGU2026_repo",
        "url": REPO_URL,
        "label": "EGU 2026 GitHub repository",
    },
]


def make_png(url: str, out_path: str) -> None:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=40,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(out_path)


def make_svg(url: str, out_path: str) -> None:
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(
        url,
        image_factory=factory,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=4,
    )
    img.save(out_path)


def main() -> None:
    for t in TARGETS:
        png_path = f"{t['name']}.png"
        svg_path = f"{t['name']}.svg"
        make_png(t["url"], png_path)
        make_svg(t["url"], svg_path)
        print(f"  {t['label']}")
        print(f"    URL: {t['url']}")
        print(f"    -> {png_path}")
        print(f"    -> {svg_path}")


if __name__ == "__main__":
    main()
