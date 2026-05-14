"""
Project: [Project name]
File: scripts/[00_short_name.py]
Author: [Name]
Created: YYYY-MM-DD
Last updated: YYYY-MM-DD

Purpose:
    [State what this script does: cleaning, analysis-dataset construction,
    regression, simulation, table creation, figure creation, etc.]

Research context:
    Unit of observation:
        [e.g., household, person, village-month, firm-year]

    Sample:
        [Main sample restrictions]

    Key variables:
        - Outcome(s): [definitions, including units if relevant]
        - Treatment/exposure: [definitions]
        - Covariates: [definitions]

    Statistical purpose:
        [Exploratory, robustness check, manuscript table, pre-analysis plan output, etc.]

Raw data source:
    - Origin/source: [Where the raw data came from]
    - Access/download date: YYYY-MM-DD
    - Known issues: [Known limitations, missingness, survey quirks, etc.]

Inputs:
    - data/raw/[input_file.csv]
    - data/clean/[input_file.csv]

Outputs:
    - data/clean/[output_file.csv]
    - outputs/tables/[table_name.xlsx]
    - outputs/figures/[figure_name.png]

Assumptions:
    - [Missing-data rules]
    - [Sample restrictions]
    - [Variable definitions]
    - [Merge assumptions]
    - [Functional-form or modeling assumptions, if any]

Environment / dependencies:
    - Python version: [e.g., 3.11, if relevant]
    - Dependencies file: [requirements.txt / pyproject.toml / environment.yml]
    - Key packages: pandas, numpy, statsmodels, etc. [only if relevant]

How to run:
    python scripts/[00_short_name.py]

Notes:
    - [Known limitations, fragile steps, manual dependencies, or future improvements.]
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd

# Module-level logger: works when this file is run directly or imported by a pipeline.
LOG = logging.getLogger(__name__)

# All paths should be relative to the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

LOG_FORMAT = "%(levelname)s:%(name)s:%(message)s"

# Use a seed for simulations, sampling, bootstraps, train/test splits, or randomized models.
RANDOM_SEED = 42

INPUT_PATH = PROJECT_ROOT / "data" / "raw" / "[input_file.csv]"
OUTPUT_PATH = PROJECT_ROOT / "data" / "clean" / "[output_file.csv]"


def configure_logging() -> None:
    """Configure readable command-line logs."""
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def load_data(path: Path) -> pd.DataFrame:
    """Load input data and fail clearly if the file is missing."""
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")

    LOG.info("Loading data from %s", path)
    df = pd.read_csv(path)
    LOG.info("Loaded %s rows and %s columns", len(df), len(df.columns))
    return df


def validate_inputs(df: pd.DataFrame) -> None:
    """Check required columns and obvious data problems before processing."""
    required_columns = ["id"]  # Replace with actual required columns.
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Replace "id" with the project's true ID variable.
    if df["id"].isna().any():
        raise ValueError("Missing values found in required ID column: id")


def log_row_change(step_name: str, before_n: int, after_n: int) -> None:
    """Log row-count changes after filters, merges, restrictions, or reshaping."""
    LOG.info(
        "%s: rows before = %s; rows after = %s; rows changed = %s",
        step_name,
        before_n,
        after_n,
        after_n - before_n,
    )


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean data while preserving traceability and logging row changes."""
    df = df.copy()

    before_n = len(df)

    # Example only. Replace with project-specific logic.
    # Use .loc for assignment and .copy() for filtered subsets that will be modified.
    #
    # Good:
    # adults = df.loc[df["age"] >= 18].copy()
    # adults.loc[:, "eligible"] = 1
    #
    # Avoid chained assignment:
    # df[df["age"] >= 18]["eligible"] = 1

    after_n = len(df)
    log_row_change("clean_data", before_n, after_n)

    return df


def save_output(df: pd.DataFrame, path: Path) -> None:
    """Save output, creating the destination folder if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    LOG.info("Saved %s rows and %s columns to %s", len(df), len(df.columns), path)


def main() -> None:
    """Run the analysis script end to end."""
    configure_logging()
    np.random.seed(RANDOM_SEED)

    df = load_data(INPUT_PATH)
    validate_inputs(df)
    df_clean = clean_data(df)
    save_output(df_clean, OUTPUT_PATH)


if __name__ == "__main__":
    main()
