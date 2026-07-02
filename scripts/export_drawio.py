#!/usr/bin/env python3
import shutil
import subprocess
import sys
from pathlib import Path


DRAWIO_CANDIDATES = [
    Path("/Applications/draw.io.app/Contents/MacOS/draw.io"),
    Path("/Applications/drawio.app/Contents/MacOS/drawio"),
    Path("/usr/bin/drawio"),
    Path("/usr/local/bin/drawio"),
]


def find_drawio():
    for path in DRAWIO_CANDIDATES:
        if path.exists():
            return str(path)
    return shutil.which("drawio")


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("Usage: export_drawio.py input.drawio [output.png]", file=sys.stderr)
        return 2

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"missing: {input_path}", file=sys.stderr)
        return 1

    output_path = Path(sys.argv[2]) if len(sys.argv) == 3 else input_path.with_suffix(".png")
    drawio = find_drawio()
    if not drawio:
        print("draw.io CLI not found", file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [drawio, "-x", "-f", "png", "-s", "1", "-o", str(output_path), str(input_path)]
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode != 0:
        return result.returncode
    if not output_path.exists() or output_path.stat().st_size == 0:
        print(f"export failed: {output_path}", file=sys.stderr)
        return 1
    print(f"exported: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
