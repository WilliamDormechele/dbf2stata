from datetime import date
from pathlib import Path
import struct

import pandas as pd

from dbf2stata.core import (
    convert_dbf,
    convert_directory,
    find_dbf_files,
)


def make_test_dbf(path: Path):
    """
    Create a tiny dBase III DBF file for automated testing.

    The test DBF contains:
        PERSONID   character
        AGE        numeric
        VISITDATE  date
        ACTIVE     logical

    Field names are deliberately uppercase so that the
    lowercase conversion behaviour can be tested.
    """

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

    number_of_records = len(rows)

    header_length = (
        32
        + (32 * len(fields))
        + 1
    )

    record_length = (
        1
        + sum(
            field[2]
            for field in fields
        )
    )

    today = date.today()

    header = bytearray(32)

    # dBase III
    header[0] = 0x03

    header[1] = today.year - 1900
    header[2] = today.month
    header[3] = today.day

    header[4:8] = struct.pack(
        "<I",
        number_of_records
    )

    header[8:10] = struct.pack(
        "<H",
        header_length
    )

    header[10:12] = struct.pack(
        "<H",
        record_length
    )

    with path.open("wb") as dbf:

        # Main DBF header
        dbf.write(header)

        # Field descriptors
        for name, field_type, width, decimals in fields:

            descriptor = bytearray(32)

            encoded_name = (
                name.encode("ascii")[:11]
            )

            descriptor[
                :len(encoded_name)
            ] = encoded_name

            descriptor[11] = ord(field_type)
            descriptor[16] = width
            descriptor[17] = decimals

            dbf.write(descriptor)

        # End of field descriptors
        dbf.write(b"\x0D")

        # Records
        for personid, age, visitdate, active in rows:

            record = bytearray()

            # Active/non-deleted record marker
            record.extend(b" ")

            record.extend(
                personid
                .encode("ascii")
                .ljust(8, b" ")
            )

            record.extend(
                str(age)
                .encode("ascii")
                .rjust(3, b" ")
            )

            record.extend(
                visitdate.encode("ascii")
            )

            record.extend(
                b"T" if active else b"F"
            )

            dbf.write(record)

        # End-of-file marker
        dbf.write(b"\x1A")


def test_find_dbf_files_is_case_insensitive(tmp_path):

    (tmp_path / "one.dbf").touch()
    (tmp_path / "two.DBF").touch()
    (tmp_path / "ignore.txt").touch()

    files = find_dbf_files(tmp_path)

    assert len(files) == 2

    assert {
        item.name
        for item in files
    } == {
        "one.dbf",
        "two.DBF",
    }


def test_convert_directory_lowercases_variable_names(tmp_path):

    source = tmp_path / "source"
    output = tmp_path / "output"

    source.mkdir()

    dbf_file = source / "sample.dbf"

    make_test_dbf(dbf_file)

    results = convert_directory(
        source,
        output,
    )

    assert len(results) == 1

    result = results[0]

    assert result.success is True
    assert result.records == 2
    assert result.error is None
    assert result.output.exists()

    data = pd.read_stata(
        result.output
    )

    assert list(data.columns) == [
        "personid",
        "age",
        "visitdate",
        "active",
    ]

    assert data["personid"].tolist() == [
        "A001",
        "B002",
    ]

    assert data["age"].tolist() == [
        37,
        5,
    ]

    assert data["active"].tolist() == [
        1.0,
        0.0,
    ]

    assert (
        data.loc[0, "visitdate"]
        .date()
        .isoformat()
        == "2026-01-15"
    )

    assert (
        data.loc[1, "visitdate"]
        .date()
        .isoformat()
        == "2026-02-20"
    )


def test_keepcase_preserves_dbf_variable_names(tmp_path):

    source = tmp_path / "sample.dbf"
    output = tmp_path / "output"

    make_test_dbf(source)

    result = convert_dbf(
        source,
        output,
        lowernames=False,
    )

    assert result.success is True

    data = pd.read_stata(
        result.output
    )

    assert list(data.columns) == [
        "PERSONID",
        "AGE",
        "VISITDATE",
        "ACTIVE",
    ]


def test_existing_output_is_not_overwritten_by_default(tmp_path):

    source = tmp_path / "sample.dbf"

    make_test_dbf(source)

    first = convert_dbf(
        source
    )

    assert first.success is True

    second = convert_dbf(
        source
    )

    assert second.success is False

    assert (
        "Output already exists"
        in second.error
    )


def test_replace_allows_existing_output_to_be_overwritten(tmp_path):

    source = tmp_path / "sample.dbf"

    make_test_dbf(source)

    first = convert_dbf(
        source
    )

    assert first.success is True

    second = convert_dbf(
        source,
        replace=True,
    )

    assert second.success is True
    assert second.records == 2


def test_default_output_is_source_directory(tmp_path):

    source = tmp_path / "sample.dbf"

    make_test_dbf(source)

    result = convert_dbf(
        source
    )

    assert result.success is True

    assert result.output == (
        tmp_path / "sample.dta"
    )

    assert result.output.exists()


def test_custom_output_directory_is_created(tmp_path):

    source = tmp_path / "sample.dbf"

    output = (
        tmp_path
        / "new"
        / "stata"
        / "folder"
    )

    make_test_dbf(source)

    result = convert_dbf(
        source,
        output,
    )

    assert result.success is True
    assert output.is_dir()

    assert result.output == (
        output / "sample.dta"
    )


def test_empty_directory_returns_no_results(tmp_path):

    results = convert_directory(
        tmp_path
    )

    assert results == []


def test_missing_dbf_returns_failure(tmp_path):

    source = (
        tmp_path
        / "does_not_exist.dbf"
    )

    result = convert_dbf(
        source
    )

    assert result.success is False

    assert (
        "DBF file not found"
        in result.error
    )