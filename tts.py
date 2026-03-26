#!/usr/bin/env python3
"""
readout CLI — Convert text files to MP3 using Microsoft Edge neural voices.

Usage:
    python tts.py input.txt
    python tts.py input.txt --voice en-US-AriaNeural --rate -10% --output out.mp3
    python tts.py file1.txt file2.txt file3.txt
    python tts.py --list-voices
    python tts.py --list-voices --filter en-US
"""

import argparse
import asyncio
import sys
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print("Error: edge-tts is not installed. Run: pip install edge-tts")
    sys.exit(1)


# ─── Default Settings ────────────────────────────────────────────────────────

DEFAULT_VOICE = "en-US-EmmaNeural"
DEFAULT_RATE  = "+0%"

# Popular en-US voices for quick reference:
#   en-US-EmmaNeural    female  natural, clear
#   en-US-AriaNeural    female  versatile, expressive
#   en-US-JennyNeural   female  friendly, conversational
#   en-US-GuyNeural     male    professional
#   en-US-AndrewNeural  male    warm


# ─── Core TTS Function ───────────────────────────────────────────────────────

async def convert(text: str, output_path: Path, voice: str, rate: str) -> None:
    """Run TTS and save to MP3."""
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    await communicate.save(str(output_path))


# ─── Voice Listing ───────────────────────────────────────────────────────────

async def list_voices(filter_str: str | None = None) -> None:
    """Print available voices, optionally filtered by locale or name."""
    voices = await edge_tts.list_voices()
    if filter_str:
        voices = [v for v in voices if filter_str.lower() in v["ShortName"].lower()]

    if not voices:
        print(f"No voices found matching '{filter_str}'.")
        return

    name_w   = max(len(v["ShortName"]) for v in voices) + 2
    gender_w = 8
    locale_w = 10

    header = f"{'Voice':<{name_w}} {'Gender':<{gender_w}} {'Locale':<{locale_w}}"
    print(header)
    print("─" * len(header))
    for v in voices:
        gender = v.get("Gender", "—")
        locale = v.get("Locale", "—")
        print(f"{v['ShortName']:<{name_w}} {gender:<{gender_w}} {locale:<{locale_w}}")

    print(f"\n{len(voices)} voice(s) listed.")


# ─── Single File Conversion ───────────────────────────────────────────────────

def process_file(input_path: Path, output_path: Path | None, voice: str, rate: str) -> Path:
    """Read a text file, convert to MP3, return the output path."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if input_path.suffix.lower() != ".txt":
        raise ValueError(f"Expected a .txt file, got: {input_path.name}")

    text = input_path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"Input file is empty: {input_path.name}")

    out = output_path or input_path.with_suffix(".mp3")
    asyncio.run(convert(text, out, voice, rate))
    return out


# ─── CLI ─────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tts",
        description="readout CLI — Convert .txt files to MP3 using Microsoft Edge neural voices.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tts.py notes.txt
  python tts.py prep.txt --voice en-US-AriaNeural --rate -10%
  python tts.py file1.txt file2.txt file3.txt
  python tts.py notes.txt --output audio/notes.mp3
  python tts.py --list-voices --filter en-US
        """,
    )

    parser.add_argument(
        "inputs",
        nargs="*",
        metavar="FILE",
        help="One or more .txt files to convert",
    )
    parser.add_argument(
        "--voice", "-v",
        default=DEFAULT_VOICE,
        metavar="VOICE",
        help=f"Edge TTS voice name (default: {DEFAULT_VOICE})",
    )
    parser.add_argument(
        "--rate", "-r",
        default=DEFAULT_RATE,
        metavar="RATE",
        help='Speaking rate adjustment, e.g. "+20%%" or "-10%%" (default: +0%%)',
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        metavar="FILE",
        help="Output .mp3 path (single-file mode only)",
    )
    parser.add_argument(
        "--list-voices", "-l",
        action="store_true",
        help="List available voices and exit",
    )
    parser.add_argument(
        "--filter", "-f",
        default=None,
        metavar="STRING",
        dest="voice_filter",
        help="Filter voice list by locale or name (use with --list-voices)",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.list_voices:
        asyncio.run(list_voices(args.voice_filter))
        return

    if not args.inputs:
        parser.print_help()
        sys.exit(1)

    if args.output and len(args.inputs) > 1:
        print("Error: --output can only be used with a single input file.")
        sys.exit(1)

    errors = []
    for raw in args.inputs:
        input_path  = Path(raw)
        output_path = Path(args.output) if args.output else None
        try:
            out = process_file(input_path, output_path, args.voice, args.rate)
            print(f"✓ {input_path.name}  →  {out}")
        except (FileNotFoundError, ValueError) as e:
            print(f"✗ {input_path.name}  —  {e}")
            errors.append(raw)

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
