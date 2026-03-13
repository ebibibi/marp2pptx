"""CLI entry point: python -m marp2pptx slides.md [-o output.pptx]"""

import argparse
import sys
from pathlib import Path

from .converter import convert, check_overlaps


def main():
    parser = argparse.ArgumentParser(
        prog="marp2pptx",
        description="Convert Marp Markdown to PowerPoint with auto-sizing fonts",
    )
    parser.add_argument("input", help="Input .md file")
    parser.add_argument("-o", "--output", help="Output .pptx (default: same basename)")
    parser.add_argument("--no-check", action="store_true", help="Skip overlap check")
    args = parser.parse_args()

    inp = Path(args.input)
    if not inp.exists():
        print(f"Error: {inp} not found", file=sys.stderr)
        sys.exit(1)

    out_path, n = convert(inp, args.output)
    print(f"Created {out_path} ({n} slides)")

    if not args.no_check:
        issues = check_overlaps(out_path)
        if issues:
            print(f"\nWarning: {len(issues)} overlap(s) detected:")
            for issue in issues:
                print(f"  {issue}")
        else:
            print("No overlaps detected")


if __name__ == "__main__":
    main()
