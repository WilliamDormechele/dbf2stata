{smcl}
{* *! version 0.1.0 14aug2026}{...}
{title:dbf2stata}

{p 4 4 2}
Batch-convert DBF files to Stata .dta format using the dbf2stata Python package.

{title:Syntax}

{p 8 8 2}
{cmd:dbf2stata}
[{cmd:,} {opt inputdir(path)} {opt outputdir(path)} {opt keepcase} {opt replace}]

{title:Description}

{pstd}
{cmd:dbf2stata} converts every .dbf or .DBF file in a folder to Stata .dta format.

{pstd}
With no options, {cmd:dbf2stata} opens a file chooser. Select any DBF file in
the folder to be converted. Every DBF file in that folder is then processed.

{pstd}
By default, .dta files are saved in the same folder as the source DBFs and
variable names are converted to lowercase.

{pstd}
The Stata command uses the same Python conversion engine as the
{cmd:dbf2stata} command-line package.

{title:Requirements}

{pstd}
Stata 16 or newer with Python configured for Stata.

{pstd}
The Python environment used by Stata must have the {cmd:dbf2stata}
Python package installed.

{title:Installation}

{pstd}
First identify the Python environment used by Stata:

{p 8 8 2}{cmd:. python query}

{pstd}
The output reports the executable under {cmd:python_exec}. Install
{cmd:dbf2stata} into that Python environment using pip.

{pstd}
For example, from Windows PowerShell:

{p 8 8 2}
{cmd:& "PATH-REPORTED-BY-STATA\python.exe" -m pip install dbf2stata}

{pstd}
Then install the Stata command for release 0.1.0:

{p 8 8 2}
{cmd:. net install dbf2stata, from("https://raw.githubusercontent.com/WilliamDormechele/dbf2stata/v0.1.0/stata")}

{pstd}
Verify the Stata installation:

{p 8 8 2}{cmd:. which dbf2stata}

{p 8 8 2}{cmd:. help dbf2stata}


{title:SSC installation}

{pstd}
The package is being prepared for submission to the Statistical Software
Components (SSC) Archive. Until SSC accepts and publishes {cmd:dbf2stata},
install the versioned Stata files from GitHub as described above.

{pstd}
Once the package has been accepted and published on SSC, installation will be:

{p 8 8 2}{cmd:. ssc install dbf2stata}

{pstd}
The Python package must still be installed in the Python environment used by
Stata.

{title:Options}
{phang}
{opt inputdir(path)} specifies the folder containing the DBF files and bypasses
the file chooser.

{phang}
{opt outputdir(path)} specifies another output folder. If omitted, output is
saved in the DBF input folder.

{phang}
{opt keepcase} retains the field-name case stored in the DBF. If omitted,
variable names are converted to lowercase.

{phang}
{opt replace} overwrites existing .dta files. Without {cmd:replace}, existing
.dta files are protected from overwrite.

{title:Examples}

{pstd}
Open the file chooser:

{p 8 8 2}{cmd:. dbf2stata}

{pstd}
Specify the input folder:

{p 8 8 2}{cmd:. dbf2stata, inputdir("C:\data\dbfs")}

{pstd}
Specify another output folder:

{p 8 8 2}{cmd:. dbf2stata, inputdir("C:\data\dbfs") outputdir("C:\data\stata")}

{pstd}
Overwrite existing .dta files:

{p 8 8 2}{cmd:. dbf2stata, inputdir("C:\data\dbfs") replace}

{pstd}
Retain DBF field-name case:

{p 8 8 2}{cmd:. dbf2stata, inputdir("C:\data\dbfs") keepcase}

{title:Stored results}

{pstd}
{cmd:dbf2stata} stores the following in {cmd:r()}:

{synoptset 20 tabbed}{...}
{synopt:{cmd:r(files)}}number of DBF files found{p_end}
{synopt:{cmd:r(converted)}}number successfully converted{p_end}
{synopt:{cmd:r(failed)}}number that failed{p_end}
{synopt:{cmd:r(records)}}total records written{p_end}

{title:Author}

{pstd}
William Dormechele{p_end}

{pstd}
University of East Anglia, United Kingdom{p_end}

{title:Links}

{pstd}
Python package:
{browse "https://pypi.org/project/dbf2stata/":PyPI}{p_end}

{pstd}
Source code and issue tracker:
{browse "https://github.com/WilliamDormechele/dbf2stata":GitHub}{p_end}

{title:License}

{pstd}
MIT License.{p_end}
