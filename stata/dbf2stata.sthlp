{smcl}
{* *! version 0.1.0 14aug2026}{...}
{title:dbf2stata}

{p 4 4 2}
Convert all DBF files in a folder to Stata .dta files using the dbf2stata Python package.

{title:Syntax}

{p 8 8 2}
{cmd:dbf2stata}
[{cmd:,} {opt inputdir(path)} {opt outputdir(path)} {opt keepcase} {opt replace}]

{title:Description}

{pstd}
With no options, {cmd:dbf2stata} opens a file chooser. Select any DBF file in the
folder you want to convert. Every DBF file in that folder is then converted.

{pstd}
By default, the .dta files are saved in the same folder as the DBF files and
variable names are converted to lowercase.

{title:Options}

{phang}
{opt inputdir(path)} specifies the folder containing the DBF files and bypasses
the file chooser.

{phang}
{opt outputdir(path)} specifies another output folder. If omitted, output is
saved in the DBF input folder.

{phang}
{opt keepcase} retains the DBF field-name case. If omitted, variable names are
lowercase.

{phang}
{opt replace} overwrites existing .dta files. Without {cmd:replace}, existing
.dta files are not overwritten.

{title:Examples}

{p 8 8 2}{cmd:. dbf2stata}

{p 8 8 2}{cmd:. dbf2stata, inputdir("C:\data\dbfs")}

{p 8 8 2}{cmd:. dbf2stata, inputdir("C:\data\dbfs") outputdir("C:\data\stata")}

{p 8 8 2}{cmd:. dbf2stata, inputdir("C:\data\dbfs") replace}

{title:Requirements}

{pstd}
Stata 16 or newer and Python configured for Stata. The Python environment used
by Stata must have the {cmd:dbf2stata} Python package installed.

{title:Stored results}

{pstd}
{cmd:dbf2stata} stores the following in {cmd:r()}:

{synoptset 20 tabbed}{...}
{synopt:{cmd:r(files)}}number of DBF files found{p_end}
{synopt:{cmd:r(converted)}}number successfully converted{p_end}
{synopt:{cmd:r(failed)}}number that failed{p_end}
{synopt:{cmd:r(records)}}total records written{p_end}
