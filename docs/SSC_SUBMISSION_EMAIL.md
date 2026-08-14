# SSC submission email draft

**To:** kit.baum@bc.edu

**Subject:** SSC submission: dbf2stata - batch conversion of DBF files to Stata .dta

Dear Professor Baum,

I would like to submit `dbf2stata` for consideration for inclusion in the
Statistical Software Components (SSC) Archive.

`dbf2stata` is a Stata 16+ command for batch conversion of DBF files to Stata
`.dta` format. The command uses the public `dbf2stata` Python package as its
conversion engine and supports DBF date and datetime fields, numeric and logical
fields, character and memo fields, lowercase variable names by default,
optional preservation of DBF field-name case, selectable output directories,
and overwrite protection.

The package also includes `dbf2stata_setup`, a companion setup utility for the
external Python dependency. `dbf2stata` itself never silently installs or
upgrades Python packages. If the Python engine is missing, it gives the user a
clear message to run `dbf2stata_setup`. When explicitly invoked,
`dbf2stata_setup` uses the exact Python interpreter currently running inside
Stata, checks Python and pip, installs the supported public PyPI dependency when
needed, and verifies that the conversion engine can be imported.

The package requires Stata 16 or newer and Python 3.10 or newer configured in
Stata.

I checked the proposed package name in Stata on 14 August 2026 using
`search dbf2stata, all` and `ssc describe dbf2stata`; no existing package or
matching command was returned.

The Python package is publicly available on PyPI, and the source code is
available on GitHub. The conversion engine is automatically tested on Windows,
Linux, macOS Apple Silicon, and macOS Intel. The Stata integration and guided
dependency flow have also been tested on a licensed Stata installation on
Windows.

PyPI:
https://pypi.org/project/dbf2stata/

Source repository:
https://github.com/WilliamDormechele/dbf2stata

The software is released under the MIT License.

I have attached the four Stata package files:

- dbf2stata.ado
- dbf2stata.sthlp
- dbf2stata_setup.ado
- dbf2stata_setup.sthlp

I would be grateful if you would consider the package for inclusion in SSC.
Please let me know if any changes are required to the programs, help files,
metadata, or dependency documentation.

Best wishes,

William Dormechele
PhD Researcher
University of East Anglia
United Kingdom