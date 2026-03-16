from __future__ import annotations

import argparse
from pathlib import Path

import qrcode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gera um QR code PNG para uma URL publica.")
    parser.add_argument("url", help="URL que sera codificada no QR code.")
    parser.add_argument(
        "outputs",
        nargs="+",
        help="Um ou mais caminhos de saida para o arquivo PNG.",
    )
    parser.add_argument("--box-size", type=int, default=12, help="Tamanho de cada modulo do QR.")
    parser.add_argument("--border", type=int, default=4, help="Margem externa do QR.")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=args.box_size,
        border=args.border,
    )
    qr.add_data(args.url)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")

    for output in args.outputs:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        image.save(path)
        print(path.as_posix())


if __name__ == "__main__":
    main()