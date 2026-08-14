# dbf2stata

[![CI](https://github.com/WilliamDormechele/dbf2stata/actions/workflows/ci.yml/badge.svg)](https://github.com/WilliamDormechele/dbf2stata/actions/workflows/ci.yml)
`dbf2stata` converts DBF files to Stata `.dta` format from either Python or Stata.

It is intended for research and legacy-data workflows where DBF collections may contain mixed date, datetime, numeric, logical, character, memo, currency, or FoxPro-style fields.

## Features

- Converts every `.dbf` or `.DBF` file in a folder.
- Saves `.dta` files beside the source DBFs by default.
- Supports a separate output directory.
- Converts variable names to lowercase by default.
- `--keep-case` retains the field-name case stored in the DBF.
- Converts DBF date fields to Stata daily dates and datetime fields to Stata datetimes.
- Handles Decimal, numeric, logical, character, memo, currency, and supported binary-like fields.
- Protects existing `.dta` files from accidental overwrite unless replacement is explicitly requested.
- Reports per-file and overall conversion results.
- Provides the same conversion engine to Python and Stata users.

## Installation

### Python

Install the current release from PyPI:

```bash
pip install dbf2stata
```

Install version 0.1.0 explicitly:

```bash
pip install dbf2stata==0.1.0
```

For isolated command-line installation, `pipx` may also be used:

```bash
pipx install dbf2stata
```

Verify the installation:

```bash
dbf2stata --help
```

For local development from this repository:

```bash
python -m pip install -e .
```

### Stata

The Stata command requires:

- Stata 16 or newer.
- Python configured in Stata.
- The `dbf2stata` Python package installed in the Python environment used by Stata.

First identify the Python installation used by Stata:

```stata
python query
```

The output reports the executable under `python_exec`.

Install `dbf2stata` into that Python environment.

On Windows PowerShell:

```powershell
& "PATH-REPORTED-BY-STATA\python.exe" -m pip install dbf2stata
```

On macOS or Linux, open Terminal and run the Python executable reported by
`python query`:

```bash
"/path/reported/by/Stata/python3" -m pip install dbf2stata
```

Quoting the executable path is recommended, particularly when the path contains
spaces.

Then install the Stata command for release `v0.1.0`:

```stata
net install dbf2stata, from("https://raw.githubusercontent.com/WilliamDormechele/dbf2stata/v0.1.0/stata")
```

Verify the Stata installation:

```stata
which dbf2stata
help dbf2stata
```


### SSC installation

The Stata package is being prepared for submission to the Statistical Software
Components (SSC) Archive. Until SSC accepts and publishes the package, install
the versioned Stata files from GitHub using the `net install` command above.

Once the package has been accepted and published on SSC, installation will be:

```stata
ssc install dbf2stata
```

SSC submission preparation and the post-acceptance checklist are documented in
`docs/SSC_SUBMISSION.md`.

## Python usage
### Interactive

Run:

```bash
dbf2stata
```

The program asks for the folder containing the DBFs and then for an output folder:

```text
Folder containing DBF files: C:\data\dbfs
Output folder [press Enter to use C:\data\dbfs]:
```

Press Enter at the second prompt to save the `.dta` files beside the DBFs.

### Command-line arguments

Save output beside the DBFs:

```bash
dbf2stata "C:\data\dbfs"
```

Use another output folder:

```bash
dbf2stata "C:\data\dbfs" --output "C:\data\stata"
```

Overwrite existing `.dta` files:

```bash
dbf2stata "C:\data\dbfs" --replace
```

Keep the field-name case stored in the DBF:

```bash
dbf2stata "C:\data\dbfs" --keep-case
```

The package can also be run as a Python module:

```bash
python -m dbf2stata
```

## Stata usage

Run interactively:

```stata
dbf2stata
```

With no options, a file-selection window opens. Select any DBF file in the folder to be converted. All DBF files in that folder are processed, and the `.dta` files are saved in the same folder by default.

Specify the input folder directly:

```stata
dbf2stata, inputdir("C:\data\dbfs")
```

Specify another output folder:

```stata
dbf2stata, inputdir("C:\data\dbfs") outputdir("C:\data\stata")
```

Overwrite existing `.dta` files:

```stata
dbf2stata, inputdir("C:\data\dbfs") replace
```

Retain the field-name case stored in the DBF:

```stata
dbf2stata, inputdir("C:\data\dbfs") keepcase
```

After a conversion, Stata stores:

```stata
return list
```

with:

- `r(files)` number of DBF files found
- `r(converted)` number successfully converted
- `r(failed)` number that failed
- `r(records)` total records written


## Platform support

The Python conversion engine is platform-independent and is continuously tested
on Windows, Linux, macOS Apple Silicon, and macOS Intel.

The Stata command requires Stata 16 or newer with Python 3.10 or newer
configured. Stata supports Python integration in ado-files, and the command uses
cross-platform Stata and Python interfaces rather than Windows-specific file or
path operations.

For macOS Stata users, first run:

```stata
python query
```

Then install `dbf2stata` into that exact Python environment from Terminal:

```bash
"/path/reported/by/Stata/python3" -m pip install dbf2stata
```

The same Stata installation command is then used on macOS:

```stata
net install dbf2stata, from("https://raw.githubusercontent.com/WilliamDormechele/dbf2stata/v0.1.0/stata")
```

A portable licensed-Stata smoke test is provided in `tests/stata/`. Automated
macOS CI validates the Python engine on both Apple Silicon and Intel runners;
a real Stata-on-macOS run can be recorded separately when a licensed Mac Stata
installation is available.

## Updating
### Python

Upgrade to the latest PyPI release:

```bash
pip install --upgrade dbf2stata
```

### Stata

For a future Stata release, reinstall from the corresponding versioned GitHub location using `net install ..., replace`.

Release notes are available under `docs/releases/` and on the GitHub Releases page.

## Native Stata note

Stata itself includes `import dbase` for dBase III/IV files. `dbf2stata` is intended for batch conversion and DBF collections that benefit from additional type handling through the Python conversion engine.

## Testing

The conversion engine is covered by automated tests for:

- DBF discovery using `.dbf` and `.DBF` extensions
- lowercase variable names by default
- preservation of DBF field-name case with `--keep-case`
- numeric, logical and date conversion
- default same-folder output
- custom output directories
- overwrite protection
- explicit replacement of existing output files
- missing input-file handling

Run the automated test suite from the repository root:

```bash
python -m pytest
```

Version 0.1.0 was additionally validated on a legacy DBF collection containing 81 files and 382,566 records, including end-to-end Python, PyPI, Stata, and public-installation tests.


GitHub Actions runs the Python test suite across Python 3.10, 3.11, 3.12,
3.13, and 3.14 on Windows, Linux, and macOS Apple Silicon. Python 3.14 is also
tested on a macOS Intel runner. A separate CI job builds the source distribution
and wheel and validates both with Twine.

The Stata wrapper uses Stata's documented Python integration, Stata Function
Interface (`sfi`), operating-system file dialog, and Python `pathlib` paths.
Because GitHub-hosted runners do not include a licensed Stata installation,
licensed-Stata integration is tested separately with the portable smoke test in
`tests/stata/`.

## Project links
- PyPI: https://pypi.org/project/dbf2stata/
- Source code: https://github.com/WilliamDormechele/dbf2stata
- Releases: https://github.com/WilliamDormechele/dbf2stata/releases
- Issues: https://github.com/WilliamDormechele/dbf2stata/issues

## Author

William Dormechele

University of East Anglia, United Kingdom

## Citation

If you use `dbf2stata` in research, please cite the software using the citation metadata provided in `CITATION.cff`.

## License

MIT License. See `LICENSE`.
