version 16.0
clear all
set more off

args inputdir

if `"`inputdir'"' == "" {
    display as error "Usage:"
    display as error `"do stata_smoke.do "/path/to/dbf2stata-stata-smoke""'
    exit 198
}

display ""
display "dbf2stata licensed-Stata smoke test"
display "=================================="
display `"Input directory: `inputdir'"'
display ""

python query
which dbf2stata

capture noisily dbf2stata, inputdir(`"`inputdir'"') replace
if _rc {
    display as error "dbf2stata command failed."
    exit _rc
}

assert r(files) == 1
assert r(converted) == 1
assert r(failed) == 0
assert r(records) == 2

use `"`inputdir'/sample.dta"', clear

assert _N == 2

confirm variable personid
confirm variable age
confirm variable visitdate
confirm variable active

assert personid[1] == "A001"
assert personid[2] == "B002"
assert age[1] == 37
assert age[2] == 5
assert active[1] == 1
assert active[2] == 0

local visitfmt : format visitdate
assert substr("`visitfmt'", 1, 3) == "%td"

display ""
display "ALL LICENSED-STATA SMOKE TESTS PASSED"
display ""