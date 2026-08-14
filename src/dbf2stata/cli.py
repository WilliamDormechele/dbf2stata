from __future__ import annotations

import argparse
import os
from pathlib import Path

from .core import convert_directory


def _clean_path(value: str) -> Path:
    value = value.strip().strip('"').strip("'")
    value = os.path.expandvars(os.path.expanduser(value))
    return Path(value)


def _interactive_paths() -> tuple[Path, Path | None]:
    print("DBF to Stata converter")
    print("----------------------")

    input_text = input("Folder containing DBF files: ").strip()
    if not input_text:
        raise ValueError("A DBF input folder is required.")

    input_dir = _clean_path(input_text)
    output_text = input(
        f"Output folder [press Enter to use {input_dir}]: "
    ).strip()
    output_dir = _clean_path(output_text) if output_text else None
    return input_dir, output_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dbf2stata",
        description="Convert all DBF files in a folder to Stata .dta files.",
    )
    parser.add_argument(
        "input_dir",
        nargs="?",
        help="Folder containing DBF files. If omitted, you will be prompted.",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_dir",
        help="Output folder. Default: the DBF source folder.",
    )
    parser.add_argument(
        "--keep-case",
        action="store_true",
        help="Keep DBF field-name case. Default: convert variable names to lowercase.",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Overwrite existing .dta files.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.input_dir:
            input_dir = _clean_path(args.input_dir)
            output_dir = _clean_path(args.output_dir) if args.output_dir else None
        else:
            input_dir, prompted_output = _interactive_paths()
            output_dir = (
                _clean_path(args.output_dir)
                if args.output_dir
                else prompted_output
            )

        effective_output = output_dir if output_dir is not None else input_dir

        print(f"\nInput folder:  {input_dir}")
        print(f"Output folder: {effective_output}")
        print(
            "Variable names: "
            + ("keep DBF case" if args.keep_case else "lowercase")
        )
        print()

        results = convert_directory(
            input_dir,
            output_dir,
            lowernames=not args.keep_case,
            replace=args.replace,
        )

        if not results:
            print("No DBF files were found.")
            return 1

        successful = 0
        failed = 0
        total_records = 0

        for result in results:
            if result.success:
                successful += 1
                total_records += result.records
                print(
                    f"OK   {result.source.name} -> {result.output.name} "
                    f"({result.records:,} records)"
                )
            else:
                failed += 1
                print(f"FAIL {result.source.name}: {result.error}")

        print("\nConversion summary")
        print("------------------")
        print(f"DBF files found:       {len(results)}")
        print(f"Successfully converted: {successful}")
        print(f"Failed:                 {failed}")
        print(f"Total records written:  {total_records:,}")

        return 0 if failed == 0 else 2

    except (ValueError, FileNotFoundError, NotADirectoryError) as exc:
        parser.error(str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
