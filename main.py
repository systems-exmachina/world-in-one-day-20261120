"""Write the day's news image to /output/entry.png (Python 3.13, standard library only)."""
import os
import struct
import sys
import zlib

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
    check_chunks(data)


def check_chunks(data: bytes) -> int:
    """Walk every chunk and verify its CRC, so a damaged file stops here, not at the judge."""
    pos, count = len(PNG_SIG), 0
    while pos < len(data):
        if pos + 12 > len(data):
            sys.exit(f"entry.png: chunk header cut off at byte {pos}")
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        end = pos + 12 + length
        if end > len(data):
            sys.exit(f"entry.png: chunk at byte {pos} runs past the end of the file")
        body = data[pos + 4:pos + 8 + length]  # chunk type + chunk data
        (crc,) = struct.unpack(">I", data[pos + 8 + length:end])
        if zlib.crc32(body) != crc:
            sys.exit(f"entry.png: bad CRC in {body[:4].decode('latin-1')} chunk at byte {pos}")
        pos, count = end, count + 1
    return count


def main() -> None:
    with open(os.path.join(HERE, "entry.png"), "rb") as f:
        data = f.read()
    check_png(data)
    os.makedirs(OUT_DIR, exist_ok=True)
    # Write the same bytes on every run, so two runs always match.
    out = os.path.join(OUT_DIR, "entry.png")
    with open(out, "wb") as f:
        f.write(data)
    width, height = struct.unpack(">II", data[16:24])
    print(f"wrote {out}: {width}x{height}, {len(data)} bytes, {check_chunks(data)} chunks with valid CRCs")


if __name__ == "__main__":
    main()
