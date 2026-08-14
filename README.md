# dbf2stata

`dbf2stata` converts every `.dbf` file in a folder to a Stata `.dta` file.
It is designed for research and legacy-data workflows where DBF files contain
mixed date, numeric, logical, character, memo, or FoxPro-style fields.

## Behaviour

- Converts all DBF files in one folder.
- Saves `.dta` files in the DBF folder by default.
- Lets the user choose a different output folder.
- Converts Stata variable names to lowercase by default.
- `--keep-case` retains the DBF field-name case.
- Converts DBF date fields to Stata daily dates and datetime fields to Stata datetimes.
- Handles Decimal, numeric, logical, character, memo, and binary-like fields.
- Reports per-file and overall conversion results.

## Install for Python users

When published to PyPI:

```bash
pip install dbf2stata
```

For isolated command-line installation, `pipx` is also suitable:

```bash
pipx install dbf2stata
```

For local development from this repository:

```bash
python -m pip install -e .
```

## Run interactively

```bash
dbf2stata
```

The program asks:

```text
Folder containing DBF files: C:\data\dbfs
Output folder [press Enter to use C:\data\dbfs]:
```

Press Enter at the second prompt to save the `.dta` files beside the DBFs.

## Run with command-line arguments

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

Keep the field-name case stored in the DBF instead of lowercasing names:

```bash
dbf2stata "C:\data\dbfs" --keep-case
```

You can also run the package as a module:

```bash
python -m dbf2stata
```

## Stata command

The `stata/` directory contains:

- `dbf2stata.ado`
- `dbf2stata.sthlp`

The Stata command uses the same Python conversion engine, so Python and Stata
users receive the same type handling and output behaviour.

### Stata requirements

- Stata 16 or newer with Python configured.
- The `dbf2stata` Python package installed in the Python environment used by Stata.

Check Stata's Python configuration with:

```stata
python query
```

Once the ado package is installed, run:

```stata
dbf2stata
```

With no options, Stata asks you to select any DBF file in the folder. It then
converts every DBF in that folder and saves the `.dta` files in the same folder.

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

Retain DBF field-name case:

```stata
dbf2stata, inputdir("C:\data\dbfs") keepcase
```

## Native Stata note

Stata itself includes `import dbase` for dBase III/IV DBF files. This project is
intended for batch conversion and for DBF collections that benefit from the
additional type handling provided by the Python conversion engine.

## Suggested repository layout

```text
dbf2stata/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── dbf2stata/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       └── core.py
└── stata/
    ├── dbf2stata.ado
    └── dbf2stata.sthlp
```

## Before publishing

Replace the placeholders `YOUR NAME` and `YOUR-USERNAME` in `pyproject.toml`
and `LICENSE`.

Recommended release sequence:

1. Create a public GitHub repository named `dbf2stata`.
2. Add tests and sample DBF files that contain no sensitive data.
3. Tag a first release such as `v0.1.0`.
4. Publish the Python package to PyPI.
5. Test installation on Windows, macOS, and Linux where possible.
6. Package the `.ado` and `.sthlp` files for Stata distribution.
7. Consider submitting the Stata command to SSC after the command and help file are stable.

## License

MIT. See `LICENSE`.
