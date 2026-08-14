from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Iterable

import pandas as pd
from dbfread import DBF


@dataclass
class ConversionResult:
    source: Path
    output: Path
    records: int = 0
    success: bool = False
    error: str | None = None


def _as_text(value):
    if value is None:
        return ""
    if isinstance(value, (bytes, bytearray)):
        return value.hex()
    return str(value)


def _prepare_dataframe(table: DBF, records: list[dict]) -> tuple[pd.DataFrame, dict[str, str]]:
    field_names = list(table.field_names)
    df = pd.DataFrame(records, columns=field_names)
    convert_dates: dict[str, str] = {}

    for field in table.fields:
        variable = field.name
        if variable not in df.columns:
            continue

        if field.type == "D":
            df[variable] = pd.to_datetime(df[variable], errors="coerce")
            convert_dates[variable] = "td"

        elif field.type in ("T", "@"):
            df[variable] = pd.to_datetime(df[variable], errors="coerce")
            convert_dates[variable] = "tc"

        elif field.type == "L":
            df[variable] = df[variable].map({True: 1.0, False: 0.0})

        elif field.type == "Y":
            df[variable] = pd.to_numeric(
                df[variable].apply(lambda x: float(x) if x is not None else None),
                errors="coerce",
            )

        elif field.type in ("B", "I", "N", "F"):
            df[variable] = pd.to_numeric(df[variable], errors="coerce")

        elif field.type in ("C", "V", "M", "0", "G", "P"):
            df[variable] = df[variable].apply(_as_text)

    # Final Stata-compatibility check for any remaining object columns.
    for variable in df.columns:
        if df[variable].dtype != "object":
            continue

        non_missing = df[variable].dropna()

        if non_missing.empty:
            df[variable] = ""
            continue

        if non_missing.map(lambda x: isinstance(x, datetime)).all():
            df[variable] = pd.to_datetime(df[variable], errors="coerce")
            convert_dates[variable] = "tc"
            continue

        if non_missing.map(
            lambda x: isinstance(x, date) and not isinstance(x, datetime)
        ).all():
            df[variable] = pd.to_datetime(df[variable], errors="coerce")
            convert_dates[variable] = "td"
            continue

        if non_missing.map(lambda x: isinstance(x, Decimal)).all():
            df[variable] = pd.to_numeric(
                df[variable].apply(lambda x: float(x) if x is not None else None),
                errors="coerce",
            )
            continue

        if non_missing.map(lambda x: isinstance(x, (bytes, bytearray))).all():
            df[variable] = df[variable].apply(_as_text)
            continue

        if non_missing.map(lambda x: isinstance(x, str)).all():
            df[variable] = df[variable].apply(_as_text)
            continue

        df[variable] = df[variable].apply(_as_text)

    return df, convert_dates


def convert_dbf(
    input_file: str | Path,
    output_dir: str | Path | None = None,
    *,
    lowernames: bool = True,
    replace: bool = False,
) -> ConversionResult:
    """Convert one DBF file to a Stata .dta file."""
    source = Path(input_file).expanduser().resolve()
    destination_dir = (
        source.parent
        if output_dir is None
        else Path(output_dir).expanduser().resolve()
    )
    destination_dir.mkdir(parents=True, exist_ok=True)
    output = destination_dir / f"{source.stem}.dta"

    result = ConversionResult(source=source, output=output)

    try:
        if not source.is_file():
            raise FileNotFoundError(f"DBF file not found: {source}")

        if output.exists() and not replace:
            raise FileExistsError(
                f"Output already exists: {output}. Use --replace to overwrite it."
            )

        table = DBF(
            str(source),
            load=False,
            char_decode_errors="replace",
            lowernames=lowernames,
        )

        records: list[dict] = []
        for record in table:
            clean_record = {}
            for variable, value in dict(record).items():
                if isinstance(value, Decimal):
                    value = float(value)
                clean_record[variable] = value
            records.append(clean_record)

        df, convert_dates = _prepare_dataframe(table, records)

        df.to_stata(
            output,
            write_index=False,
            version=118,
            convert_dates=convert_dates,
        )

        result.records = len(df)
        result.success = True
        return result

    except Exception as exc:
        result.error = str(exc)
        return result


def find_dbf_files(folder: str | Path) -> list[Path]:
    """Find DBF files in one directory, case-insensitively."""
    directory = Path(folder).expanduser().resolve()
    if not directory.is_dir():
        raise NotADirectoryError(f"Folder not found: {directory}")

    return sorted(
        [p for p in directory.iterdir() if p.is_file() and p.suffix.lower() == ".dbf"],
        key=lambda p: p.name.casefold(),
    )


def convert_directory(
    input_dir: str | Path,
    output_dir: str | Path | None = None,
    *,
    lowernames: bool = True,
    replace: bool = False,
) -> list[ConversionResult]:
    """Convert every DBF file in a directory to Stata format."""
    source_dir = Path(input_dir).expanduser().resolve()
    dbf_files = find_dbf_files(source_dir)

    if not dbf_files:
        return []

    return [
        convert_dbf(
            dbf_file,
            output_dir,
            lowernames=lowernames,
            replace=replace,
        )
        for dbf_file in dbf_files
    ]
