# SSC submission preparation for dbf2stata

## Current status

`dbf2stata` is publicly available from PyPI and GitHub. The Stata package is
ready for SSC review, subject to the archive maintainer's acceptance.

A Stata search performed on 14 August 2026 returned no match for `dbf2stata`,
and `ssc describe dbf2stata` returned `r(601)`, indicating that the package name
was not present on SSC at the time of the pre-submission check.

The immutable pre-SSC candidate can be installed with:

```stata
net install dbf2stata, from("https://raw.githubusercontent.com/WilliamDormechele/dbf2stata/ssc-candidate-2026-08-14-r4/stata")
```

After SSC acceptance and publication:

```stata
ssc install dbf2stata
```


## Intended user installation flow

Before SSC publication:

```stata
net install dbf2stata, from("https://raw.githubusercontent.com/WilliamDormechele/dbf2stata/ssc-candidate-2026-08-14-r4/stata")
dbf2stata
```

After SSC publication:

```stata
ssc install dbf2stata
dbf2stata
```

If the Python dependency is missing, `dbf2stata` then tells the user to run:

```stata
dbf2stata_setup
```

After setup, the user reruns:

```stata
dbf2stata
```

This makes the first command after installation explicit while keeping Python
dependency installation opt-in rather than silent.

## Commands supplied
The package supplies two user-facing Stata commands:

### `dbf2stata`

Batch-converts DBF files to Stata `.dta` files.

Before conversion it checks whether its external Python engine is importable.
It never silently installs or upgrades a Python package.

### `dbf2stata_setup`

A companion, explicitly invoked setup utility.

It:

- identifies the exact Python executable running inside Stata;
- requires Python 3.10 or newer;
- checks pip;
- checks whether the public `dbf2stata` Python package is available;
- installs `dbf2stata>=0.1.0,<0.2.0` from PyPI if it is missing;
- verifies that the conversion engine imports successfully.

Because the user explicitly types `dbf2stata_setup`, the external dependency is
not installed silently.

## Proposed SSC metadata

**Package name:** dbf2stata

**Title:** DBF2STATA: Stata module to batch-convert DBF files to Stata .dta format

**Author:** William Dormechele

**Affiliation:** University of East Anglia, United Kingdom

**Abstract:** `dbf2stata` batch-converts DBF files in a directory to Stata
`.dta` format using the public `dbf2stata` Python package as its conversion
engine. It supports DBF date and datetime fields, numeric and logical fields,
character and memo fields, lowercase variable names by default, optional
preservation of DBF field-name case, user-selected output directories, and
overwrite protection. The companion `dbf2stata_setup` command checks Stata's
configured Python environment and, when explicitly invoked by the user, installs
the required public PyPI dependency into that same environment.

**Requires:** Stata 16 or newer; Python 3.10 or newer configured for Stata.

**External Python dependency:** https://pypi.org/project/dbf2stata/

**Source repository:** https://github.com/WilliamDormechele/dbf2stata

**Issue tracker:** https://github.com/WilliamDormechele/dbf2stata/issues

**License:** MIT

**Keywords:** DBF; dBase; FoxPro; Stata; Python; data conversion; legacy data;
batch conversion

## Platform support

The Python engine is automatically tested on:

- Windows
- Linux
- macOS Apple Silicon
- macOS Intel

The setup mechanism uses `sys.executable -m pip`, rather than an
operating-system-specific Python path.

The Stata wrapper uses Stata's Python integration, `sfi`, the operating
system's standard file dialog, and Python cross-platform path handling.

The Windows licensed-Stata integration has been tested directly. A portable
licensed-Stata smoke test is available for additional installations, including
Stata for Mac.

## SSC files to submit

Attach these four files:

- `dbf2stata.ado`
- `dbf2stata.sthlp`
- `dbf2stata_setup.ado`
- `dbf2stata_setup.sthlp`

## Submission recipient

Christopher F. Baum
Boston College

Email:

```text
kit.baum@bc.edu
```

Review the current SSC submission guidance immediately before sending.

## Submission email

A prepared email is stored in:

```text
docs/SSC_SUBMISSION_EMAIL.md
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

## Final pre-submission checklist

- [x] Public GitHub repository.
- [x] Public PyPI package.
- [x] MIT licence.
- [x] Automated unit tests.
- [x] Python package build and Twine validation.
- [x] Windows licensed-Stata smoke test.
- [x] Public GitHub/net-install test.
- [x] Windows/Linux/macOS Python CI.
- [x] Package-name search returned no match on 14 August 2026.
- [x] `ssc describe dbf2stata` returned not found on 14 August 2026.
- [x] Guided Python dependency setup implemented.
- [ ] Guided dependency setup passes the final licensed-Stata smoke test.
- [ ] Review current SSC submission guidance immediately before sending.
- [ ] Email the four Stata files for SSC review.
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
which dbf2stata_setup
help dbf2stata
help dbf2stata_setup
dbf2stata_setup
```

Then run a real conversion and inspect:

```stata
return list
```