*! dbf2stata 0.1.0 14aug2026
*! Author: William Dormechele
*! Repository: https://github.com/WilliamDormechele/dbf2stata
*! Python package: https://pypi.org/project/dbf2stata/

capture program drop dbf2stata

program define dbf2stata, rclass
    version 16.0

    syntax [, INPUTDir(string) OUTPUTDir(string) KEEPCASE REPLACE]

    local selected ""

    /*
        If inputdir() is omitted, allow the user to select
        any DBF file. The parent folder becomes the input folder.
    */
    if `"`inputdir'"' == "" {

        capture window fopen DBF2STATA_FILE ///
            "Select any DBF file in the folder to convert" ///
            "dBase files (*.dbf)|*.dbf|All files (*.*)|*.*" dbf

        if _rc != 0 {
            exit _rc
        }

        local selected `"$DBF2STATA_FILE"'
        macro drop DBF2STATA_FILE
    }

    /*
        Default:
        - variable names are lowercase
        - existing .dta files are not overwritten
    */
    local lowernames = cond("`keepcase'" == "", "1", "0")
    local doreplace  = cond("`replace'"  == "", "0", "1")

    /*
        Run the Python conversion function defined below.
    */
    python: dbf2stata_run()

    /*
        Return conversion results to Stata.
    */
    return scalar files     = real("`dbf2stata_found'")
    return scalar converted = real("`dbf2stata_success'")
    return scalar failed    = real("`dbf2stata_failed'")
    return scalar records   = real("`dbf2stata_records'")

end


/*
    Python implementation used by the Stata command.
*/

version 16.0

python:

from pathlib import Path
from sfi import Macro, SFIToolkit


def _clean_stata_path(value):
    """Remove surrounding quotation marks passed from Stata."""

    value = (value or "").strip()

    while (
        len(value) >= 2
        and value[0] == '"'
        and value[-1] == '"'
    ):
        value = value[1:-1].strip()

    return value


def dbf2stata_run():

    try:
        from dbf2stata.core import convert_directory

    except ImportError as exc:
        raise RuntimeError(
            "The Python package 'dbf2stata' is not installed "
            "in the Python environment used by Stata. "
            "Run 'python query' in Stata to identify that Python "
            "environment, install dbf2stata there with pip, "
            "and rerun the command."
        ) from exc

    input_dir = _clean_stata_path(
        Macro.getLocal("inputdir")
    )

    selected = _clean_stata_path(
        Macro.getLocal("selected")
    )

    output_dir = _clean_stata_path(
        Macro.getLocal("outputdir")
    )

    lowernames = (
        Macro.getLocal("lowernames") == "1"
    )

    replace = (
        Macro.getLocal("doreplace") == "1"
    )

    if not input_dir:

        if not selected:
            raise RuntimeError(
                "No DBF input folder was specified."
            )

        input_dir = str(
            Path(selected)
            .expanduser()
            .resolve()
            .parent
        )

    output_arg = (
        output_dir
        if output_dir
        else None
    )

    results = convert_directory(
        input_dir,
        output_arg,
        lowernames=lowernames,
        replace=replace,
    )

    success = sum(
        result.success
        for result in results
    )

    failed = (
        len(results) - success
    )

    records = sum(
        result.records
        for result in results
        if result.success
    )

    SFIToolkit.displayln("")

    SFIToolkit.displayln(
        "DBF to Stata conversion"
    )

    SFIToolkit.displayln(
        "-----------------------"
    )

    SFIToolkit.displayln(
        f"Input folder: {input_dir}"
    )

    SFIToolkit.displayln(
        "Output folder: "
        f"{output_dir if output_dir else input_dir}"
    )

    SFIToolkit.displayln(
        "Variable names: "
        + (
            "lowercase"
            if lowernames
            else "keep DBF case"
        )
    )

    SFIToolkit.displayln("")

    for result in results:

        if result.success:

            SFIToolkit.displayln(
                f"OK   {result.source.name} "
                f"-> {result.output.name} "
                f"({result.records:,} records)"
            )

        else:

            SFIToolkit.displayln(
                f"FAIL {result.source.name}: "
                f"{result.error}"
            )

    SFIToolkit.displayln("")

    SFIToolkit.displayln(
        f"DBF files found:        "
        f"{len(results)}"
    )

    SFIToolkit.displayln(
        f"Successfully converted: "
        f"{success}"
    )

    SFIToolkit.displayln(
        f"Failed:                 "
        f"{failed}"
    )

    SFIToolkit.displayln(
        f"Total records written:  "
        f"{records:,}"
    )

    Macro.setLocal(
        "dbf2stata_found",
        str(len(results))
    )

    Macro.setLocal(
        "dbf2stata_success",
        str(success)
    )

    Macro.setLocal(
        "dbf2stata_failed",
        str(failed)
    )

    Macro.setLocal(
        "dbf2stata_records",
        str(records)
    )


end
