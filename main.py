"""Write the day's news image to /output/entry.png (Python 3.13, standard library only)."""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
MAX_BYTES = 1048576  # 1 MiB
MAX_SIDE = 1024
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def check_png(data: bytes) -> None:
    """Stop with a clear message if the image breaks the contest's limits."""
    if len(data) > MAX_BYTES:
        sys.exit(f"entry.png is {len(data)} bytes; the limit is {MAX_BYTES}")
    if not data.startswith(PNG_SIG) or data[12:16] != b"IHDR":
        sys.exit("entry.png is not a PNG with an IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        sys.exit(f"entry.png is {width}x{height}; the limit is {MAX_SIDE}x{MAX_SIDE}")
    if not data.endswith(b"IEND\xaeB`\x82"):
        sys.exit("entry.png does not end with an IEND chunk")


def main() -> None:
    with open(os.path.join(HERE, "entry.png"), "rb") as f:
        data = f.read()
    check_png(data)
    os.makedirs(OUT_DIR, exist_ok=True)
    # Write the same bytes on every run, so two runs always match.
    with open(os.path.join(OUT_DIR, "entry.png"), "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
