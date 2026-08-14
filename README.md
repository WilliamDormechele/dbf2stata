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
- Provides a guided Stata setup command for the external Python dependency.

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

Requirements:

- Stata 16 or newer.
- Python 3.10 or newer configured in Stata.

Until the SSC package is published, install the immutable SSC candidate:

```stata
net install dbf2stata, from("https://raw.githubusercontent.com/WilliamDormechele/dbf2stata/ssc-candidate-2026-08-14/stata")
```

Then simply run:

```stata
dbf2stata
```

Before opening a DBF file, the command checks whether the required Python engine is available.

If everything is ready, conversion starts normally.

If the Python package is missing, `dbf2stata` stops and tells the user exactly what to run:

```stata
dbf2stata_setup
```

`dbf2stata_setup` then:

1. uses the exact Python interpreter already running inside Stata;
2. checks that Python 3.10 or newer is available;
3. checks that `pip` is available;
4. checks whether the `dbf2stata` Python package is installed;
5. installs the supported `dbf2stata` package from PyPI when it is missing;
6. verifies that the conversion engine imports successfully;
7. reports that setup is ready.

Then rerun:

```stata
dbf2stata
```

The main `dbf2stata` command never silently installs or upgrades Python packages. Installation happens only when the user explicitly runs `dbf2stata_setup`.

To inspect Stata's Python configuration manually:

```stata
python query
```

To request an upgrade within the supported 0.1.x Python-package series:

```stata
dbf2stata_setup, upgrade
```

### SSC installation

The Stata package is being submitted to the Statistical Software Components (SSC) Archive.

After SSC accepts and publishes the package, installation will be:

```stata
ssc install dbf2stata
```

The user will then type:

```stata
dbf2stata
```

If the external Python engine is not ready, the command will direct the user to:

```stata
dbf2stata_setup
```

SSC preparation material is documented in `docs/SSC_SUBMISSION.md`.

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

After a conversion:

```stata
return list
```

`dbf2stata` stores:

- `r(files)` number of DBF files found
- `r(converted)` number successfully converted
- `r(failed)` number that failed
- `r(records)` total records written

## Platform support

The Python conversion engine is continuously tested on:

- Windows
- Linux
- macOS Apple Silicon
- macOS Intel

The Stata wrapper uses Stata's Python integration, the Stata Function Interface (`sfi`), the operating system's standard file dialog, and Python `pathlib` paths.

The guided setup command is also cross-platform. It calls:

```text
sys.executable -m pip
```

so it uses the exact Python interpreter currently used by Stata. It does not hard-code a Windows, macOS, or Linux Python path.

The Windows licensed-Stata integration has been tested directly. The repository also contains a portable licensed-Stata smoke test that can be run on additional installations, including Stata for Mac.

## Updating

### Python

Upgrade the Python command-line package:

```bash
pip install --upgrade dbf2stata
```

### Stata setup dependency

From Stata:

```stata
dbf2stata_setup, upgrade
```

### Stata command

Before SSC publication, reinstall the current SSC candidate with:

```stata
net install dbf2stata, from("https://raw.githubusercontent.com/WilliamDormechele/dbf2stata/ssc-candidate-2026-08-14/stata") replace
```

After SSC publication:

```stata
ssc install dbf2stata, replace
```

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

Run:

```bash
python -m pytest
```

Version 0.1.0 was additionally validated on a legacy DBF collection containing 81 files and 382,566 records.

GitHub Actions tests Python 3.10, 3.11, 3.12, 3.13, and 3.14 across Windows, Linux, and macOS Apple Silicon, with an additional macOS Intel job.

The guided dependency flow is tested separately on licensed Stata by temporarily removing the Python package, confirming that `dbf2stata` directs the user to setup, running `dbf2stata_setup`, and then completing a real DBF conversion.

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