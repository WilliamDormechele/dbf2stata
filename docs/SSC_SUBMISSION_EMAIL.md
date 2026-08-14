# SSC submission email draft

**To:** kit.baum@bc.edu

**Subject:** SSC submission: dbf2stata - batch conversion of DBF files to Stata .dta

Dear Professor Baum,

I would like to submit `dbf2stata` for consideration for inclusion in the
Statistical Software Components (SSC) Archive.

`dbf2stata` is a Stata 16+ command for batch conversion of DBF files to Stata
`.dta` format. The Stata command uses the public `dbf2stata` Python package as
its conversion engine and supports DBF date and datetime fields, numeric and
logical fields, character and memo fields, lowercase variable names by default,
optional preservation of DBF field-name case, selectable output directories,
and overwrite protection.

The command requires Python 3.10 or newer configured in Stata and the
`dbf2stata` Python package installed in that same Python environment.

I checked the proposed command name in Stata on 14 August 2026 using
`search dbf2stata, all` and `ssc describe dbf2stata`; no existing SSC package
was returned.

The project is released under the MIT License.

Public Python package:
https://pypi.org/project/dbf2stata/

Source repository:
https://github.com/WilliamDormechele/dbf2stata

The Python conversion engine is continuously tested on Windows, Linux, macOS
Apple Silicon, and macOS Intel. The Stata integration has also passed
licensed-Stata and public-installation smoke tests on Windows.

I have attached the two core Stata package files:

- dbf2stata.ado
- dbf2stata.sthlp

I would be grateful if you would consider the package for inclusion in SSC.
Please let me know if you would like any changes to the package, metadata, help
file, or dependency documentation.

Best wishes,

William Dormechele
University of East Anglia
United Kingdom