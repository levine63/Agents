* Date: 2026-05-06
* Author: [Name]
* Purpose: [What this do-file does and for whom]
* Inputs:
*   - [Raw dataset or source]
*   - [Supporting lookup or config]
* Outputs:
*   - [Cleaned dataset, table, figure, log]
* Setup:
*   - Stata version [version]
*   - User-written packages: [package list]
* Usage:
*   - do [script_name].do
* Assumptions:
*   - [Important assumption or scope limit]
* Not Yet Done:
*   - [Open item, unresolved check, deferred work]

version 18
set more off
* set seed 123456789

clear all

* Centralize paths here rather than scattering them below.
local project_root "."
local data_dir "`project_root'/data"
local output_dir "`project_root'/outputs"

capture mkdir "`output_dir'"

* Replace with actual input file.
local input_file "`data_dir'/example_input.dta"

confirm file "`input_file'"
use "`input_file'", clear

display "Initial N = " _N

* Replace this section with actual cleaning or analysis steps.
* Log N after filters, merges, or deduplication steps.

* Example:
* keep if sample_flag == 1
* display "Post-filter N = " _N

* Example merge pattern:
* merge 1:1 id using "`data_dir'/lookup.dta"
* tab _merge
* assert inlist(_merge, 3)
* drop _merge

* Replace with actual output.
save "`output_dir'/example_output.dta", replace
display "Saved output to `output_dir'/example_output.dta"
