# SSC submission preparation for dbf2stata

## Status

`dbf2stata` is publicly available from PyPI and GitHub. The Stata component is
being prepared for submission to the Statistical Software Components (SSC)
Archive.

Until SSC accepts and publishes the package, Stata users should install the
versioned Stata files from GitHub:

```stata
net install dbf2stata, from("https://raw.githubusercontent.com/WilliamDormechele/dbf2stata/v0.1.0/stata")
```

After acceptance on SSC, the normal installation command will be:

```stata
ssc install dbf2stata
```

Do not advertise `ssc install dbf2stata` as currently available until the SSC
Archive has accepted and published the package.

## Proposed SSC metadata

**Package name:** dbf2stata

**Title:** DBF2STATA: Stata module to batch-convert DBF files to Stata .dta format

**Author:** William Dormechele

**Affiliation:** University of East Anglia, United Kingdom

**Abstract:** `dbf2stata` batch-converts DBF files in a directory to Stata
`.dta` format. The Stata command calls the `dbf2stata` Python conversion engine
and supports DBF date and datetime fields, numeric and logical fields,
character and memo fields, lowercase variable names by default, optional
preservation of DBF field-name case, user-selected output directories, and
overwrite protection. With no options, the command opens a file chooser and
converts all DBF files in the selected file's directory.

**Requires:** Stata 16 or newer; Python configured for Stata; the `dbf2stata`
Python package installed in the Python environment used by Stata.

**External Python dependency:** https://pypi.org/project/dbf2stata/

**Source repository:** https://github.com/WilliamDormechele/dbf2stata

**License:** MIT

**Keywords:** DBF; dBase; FoxPro; Stata; Python; data conversion; legacy data;
batch conversion

## Installation files for SSC

- `dbf2stata.ado`
- `dbf2stata.sthlp`

The repository also contains `dbf2stata.pkg` and `stata.toc` for direct
versioned installation from GitHub. SSC maintains its own archive metadata,
so the core SSC installation files are the ado and help files.

## Pre-submission checklist

- [ ] `dbf2stata.ado` contains a version line and Stata `version` statement.
- [ ] `dbf2stata.sthlp` documents syntax, options, requirements, installation,
      author, links, and license.
- [ ] Python dependency on PyPI is public and tested.
- [ ] GitHub repository and release are public.
- [ ] Automated Python tests pass.
- [ ] Stata wrapper smoke test passes.
- [ ] Package name is checked against existing SSC commands immediately before
      submission.
- [ ] SSC submission guidance is reviewed immediately before sending the files.
- [ ] Submit the package to the SSC archive maintainer following the current
      SSC submission guidance.
- [ ] After acceptance, verify `ssc describe dbf2stata`.
- [ ] After acceptance, verify `ssc install dbf2stata, replace`.
- [ ] Update README/help text to state that SSC installation is live.

## Submission bundle

Run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\scripts\build_ssc_bundle.ps1"
```

The bundle will be created under:

```text
dist\ssc\dbf2stata-ssc-submission.zip
```

## Post-acceptance Stata verification

Once SSC confirms publication:

```stata
capture ado uninstall dbf2stata
ssc install dbf2stata, replace
which dbf2stata
help dbf2stata
```

Then run a real DBF conversion and inspect `return list`.
