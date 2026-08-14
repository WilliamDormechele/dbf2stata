from __future__ import annotations

from datetime import date
from pathlib import Path
import argparse
import struct


def make_test_dbf(path: Path) -> None:
    fields = [
        ("PERSONID", "C", 8, 0),
        ("AGE", "N", 3, 0),
        ("VISITDATE", "D", 8, 0),
        ("ACTIVE", "L", 1, 0),
    ]

    rows = [
        ("A001", 37, "20260115", True),
        ("B002", 5, "20260220", False),
    ]

    header_length = 32 + (32 * len(fields)) + 1
    record_length = 1 + sum(field[2] for field in fields)

    today = date.today()
    header = bytearray(32)
    header[0] = 0x03
    header[1] = today.year - 1900
    header[2] = today.month
    header[3] = today.day
    header[4:8] = struct.pack("<I", len(rows))
    header[8:10] = struct.pack("<H", header_length)
    header[10:12] = struct.pack("<H", record_length)

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("wb") as dbf:
        dbf.write(header)

        for name, field_type, width, decimals in fields:
            descriptor = bytearray(32)
            encoded_name = name.encode("ascii")[:11]
            descriptor[: len(encoded_name)] = encoded_name
            descriptor[11] = ord(field_type)
            descriptor[16] = width
            descriptor[17] = decimals
            dbf.write(descriptor)

        dbf.write(b"\x0D")

        for personid, age, visitdate, active in rows:
            record = bytearray()
            record.extend(b" ")
            record.extend(personid.encode("ascii").ljust(8, b" "))
            record.extend(str(age).encode("ascii").rjust(3, b" "))
            record.extend(visitdate.encode("ascii"))
            record.extend(b"T" if active else b"F")
            dbf.write(record)

        dbf.write(b"\x1A")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a tiny DBF fixture for the dbf2stata Stata smoke test."
    )
    parser.add_argument(
        "output_dir",
        type=Path,
        help="Directory in which sample.dbf will be created.",
    )
    args = parser.parse_args()

    output_dir = args.output_dir.expanduser().resolve()
    dbf_path = output_dir / "sample.dbf"
    dta_path = output_dir / "sample.dta"

    output_dir.mkdir(parents=True, exist_ok=True)

    if dta_path.exists():
        dta_path.unlink()

    make_test_dbf(dbf_path)

    print(f"Created: {dbf_path}")
    print("Expected records: 2")


if __name__ == "__main__":
    main()