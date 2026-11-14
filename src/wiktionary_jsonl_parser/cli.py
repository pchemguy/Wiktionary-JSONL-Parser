"""Command-line entry point for the Wiktionary JSONL converter."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from .importer import ImportFailure, import_jsonl


def positive_batch_size(value: str) -> int:
    try:
        size = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "batch size must be a positive integer"
        ) from exc
    if size < 1:
        raise argparse.ArgumentTypeError("batch size must be a positive integer")
    return size


def report_progress(chunk: int, processed: int, total: int) -> None:
    """Print a byte-based progress update to standard error."""

    tenths = processed * 1000 // total
    line = (
        f"{processed}/{total} bytes read and processed ({tenths // 10}.{tenths % 10}%)"
    )
    print(f"[chunk {chunk}] {line}", file=sys.stderr, flush=True)


def report_warning(message: str) -> None:
    print(f"warning: {message}", file=sys.stderr, flush=True)


def confirm_one_worker() -> bool:
    if sys.stdin is None or not sys.stdin.isatty():
        return False
    print("Run with one worker? [y/N]", file=sys.stderr, flush=True)
    return sys.stdin.readline().strip().casefold() in {"y", "yes"}


def main(argv: Sequence[str] | None = None) -> int:
    """Convert an extracted JSONL file and return its CLI exit status."""

    parser = argparse.ArgumentParser(
        prog="wiktionary-jsonl-parser",
        description="Import an extracted Russian Wiktionary JSONL file into SQLite.",
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, metavar="PATH")
    parser.add_argument(
        "--batch-size",
        type=positive_batch_size,
        default=10_000,
        metavar="N",
        help="maximum source lines per worker batch (default: %(default)s)",
    )
    parser.add_argument(
        "--no-progress", action="store_true", help="suppress batch progress on stderr"
    )
    args = parser.parse_args(argv)
    source = args.input
    destination = args.output
    if destination is None:
        if source.suffix != ".jsonl":
            parser.error("--output is required when INPUT has no final .jsonl suffix")
        destination = source.with_suffix(".sqlite")
    try:
        import_jsonl(
            source,
            destination,
            args.batch_size,
            on_warning=report_warning,
            confirm_single_worker=confirm_one_worker,
            on_progress=None if args.no_progress else report_progress,
        )
    except ImportFailure as exc:
        print(f"{parser.prog}: {exc}", file=sys.stderr)
        for note in getattr(exc, "__notes__", ()):
            print(note, file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print(f"{parser.prog}: interrupted", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
