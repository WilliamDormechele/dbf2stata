# SSC submission preparation for dbf2stata

## Current status

`dbf2stata` is publicly available from PyPI and GitHub. The Stata component is
ready for submission to the Statistical Software Components (SSC) Archive,
subject to the archive maintainer's review and acceptance.

A Stata search performed on 14 August 2026 returned no match for `dbf2stata`,
and `ssc describe dbf2stata` returned `r(601)`, indicating that the package name
was not present on SSC at the time of the pre-submission check.

Until SSC accepts and publishes the package, Stata users should install the
versioned files from GitHub:

```stata
net install dbf2stata, from("https://raw.githubusercontent.com/WilliamDormechele/dbf2stata/v0.1.0/stata")
```

After SSC acceptance and publication:

```stata
ssc install dbf2stata
```

## Proposed SSC metadata

**Package name:** dbf2stata

**Title:** DBF2STATA: Stata module to batch-convert DBF files to Stata .dta format

**Author:** William Dormechele

**Affiliation:** University of East Anglia, United Kingdom

**Abstract:** `dbf2stata` batch-converts DBF files in a directory to Stata
`.dta` format. The Stata command uses the public `dbf2stata` Python package as
its conversion engine. It supports DBF date and datetime fields, numeric and
logical fields, character and memo fields, lowercase variable names by default,
optional preservation of DBF field-name case, user-selected output directories,
and overwrite protection. With no options, the command opens the operating
system's standard file chooser and converts all DBF files in the selected
file's directory.

**Requires:** Stata 16 or newer; Python 3.10 or newer configured for Stata; the
`dbf2stata` Python package installed in the Python environment used by Stata.

**External Python dependency:** https://pypi.org/project/dbf2stata/

**Source repository:** https://github.com/WilliamDormechele/dbf2stata

**Issue tracker:** https://github.com/WilliamDormechele/dbf2stata/issues

**License:** MIT

**Keywords:** DBF; dBase; FoxPro; Stata; Python; data conversion; legacy data;
batch conversion

## Platform support

The conversion engine uses `pathlib`, pandas, and dbfread and contains no
Windows-specific path logic. Continuous integration tests the Python package on:

- Windows
- Linux
- macOS Apple Silicon
- macOS Intel

The Stata wrapper uses Stata's documented Python integration, `sfi`, and
`window fopen`. The portable licensed-Stata smoke test is under `tests/stata/`.

The Windows Stata integration has been tested on a licensed Stata installation.
The Python engine is automatically tested on macOS Apple Silicon and Intel.
Until a licensed Stata-on-macOS run has also been performed, do not describe
that final integration layer as independently validated on macOS; describe it
as supported by the cross-platform implementation and macOS engine tests.

## SSC files to submit

The core installation files are:

- `dbf2stata.ado`
- `dbf2stata.sthlp`

The GitHub-specific `dbf2stata.pkg` and `stata.toc` files do not need to be sent
as core SSC installation files. License and repository information are already
documented in the help file and public source repository.

## Submission recipient

The current Boston College faculty page for Christopher F. Baum lists:

```text
kit.baum@bc.edu
```

The indexed SSC submission guidance is `SSCSUBMIT`, Statistical Software
Components S436501, revised 2 May 2022. Review the live/current SSC submission
guidance immediately before sending.

## Submission email

A prepared email is stored in:

```text
docs/SSC_SUBMISSION_EMAIL.md
```

Attach:

```text
dbf2stata.ado
dbf2stata.sthlp
```

## Build the submission bundle

Run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\scripts\build_ssc_bundle.ps1"
```

Output:

```text
dist\ssc\dbf2stata-ssc-submission.zip
```

The ZIP is for convenient review/submission preparation. The two Stata files
listed above are the core package files.

## Final pre-submission checklist

- [x] Public GitHub repository.
- [x] Public PyPI package.
- [x] MIT licence.
- [x] Automated unit tests.
- [x] Python package build and Twine validation.
- [x] Windows licensed-Stata smoke test.
- [x] Public GitHub/net-install test.
- [x] Package-name search returned no match on 14 August 2026.
- [x] `ssc describe dbf2stata` returned not found on 14 August 2026.
- [ ] macOS Python CI passes after the macOS matrix is added.
- [ ] Optional but desirable: licensed Stata smoke test on macOS.
- [ ] Review current `SSCSUBMIT` guidance immediately before sending.
- [ ] Email `dbf2stata.ado` and `dbf2stata.sthlp` for SSC review.
- [ ] Await SSC acceptance/publication.
- [ ] After acceptance, verify `ssc describe dbf2stata`.
- [ ] After acceptance, verify `ssc install dbf2stata, replace`.
- [ ] Update README/help text to state that SSC installation is live.

## Post-acceptance verification

Once SSC confirms publication:

```stata
capture ado uninstall dbf2stata
ssc install dbf2stata, replace
which dbf2stata
help dbf2stata
```

Then run a real DBF conversion and inspect:

```stata
return list
```