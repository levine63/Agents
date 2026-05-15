* ***************************************************************************
* Project: [Project Name]
* File: scripts/[file_name.do]
* Author: [Name]
* Created: YYYY-MM-DD
* Last updated: YYYY-MM-DD
*
* Purpose:
*   [State whether this do-file cleans data, builds an analysis dataset,
*   runs models, or creates tables/figures.]
*
* Inputs:
*   - data/raw/[input_file].dta
*   - [Supporting lookup / config / using dataset]
*
* Outputs:
*   - data/clean/[output_file].dta
*   - outputs/[table_or_figure]
*   - [Log or side effects]
*
* Assumptions:
*   - [Sample restriction / merge assumption / required permissions]
*
* Setup:
*   - Stata version 18
*   - User-written packages: [package list]
*
* Usage:
*   - do scripts/[file_name.do]
*
* Notes:
*   - [Known limitations, fragile steps, or open questions]
* ***************************************************************************

version 18
clear all
set more off
* set seed 123456789

* Use relative paths through local macros rather than hard-coded machine paths.
local project_root "."
local raw_data "`project_root'/data/raw"
local clean_data "`project_root'/data/clean"
local output_dir "`project_root'/outputs"

capture mkdir "`clean_data'"
capture mkdir "`output_dir'"

* Linting:
* If repkit is available, run:
*   repkit lint scripts/[file_name.do]
*
* Install if needed:
*   net install repkit, from("https://raw.githubusercontent.com/worldbank/repkit/main")

local input_file "`raw_data'/[input_file].dta"

confirm file "`input_file'"
use "`input_file'", clear

display "Initial N = " _N

* Replace this section with actual cleaning or analysis steps.
* Log N after filters, merges, deduplication, and sample restrictions.

* Example filter:
* keep if sample_flag == 1
* display "Post-filter N = " _N

* Example merge pattern:
* merge 1:1 id using "`raw_data'/lookup.dta"
* tab _merge
* assert inlist(_merge, 3)
* drop _merge
* display "Post-merge N = " _N

* Replace with actual output path. Do not overwrite raw data.
save "`clean_data'/[output_file].dta", replace
display "Saved output to `clean_data'/[output_file].dta"
