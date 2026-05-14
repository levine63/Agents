"""
Project: [Project name]
File: scripts/[00_short_name.py]
Author: [Name]
Created: YYYY-MM-DD
Last updated: YYYY-MM-DD

Purpose:
    [State what this script does and why it exists.]

Inputs:
    - [List input files, folders, APIs, environment variables, or command-line arguments.]

Outputs / side effects:
    - [List output files, logs, database changes, API calls, emails sent, Drive updates, etc.]

Assumptions:
    - [Runtime assumptions, permissions, expected folder structure, API access, etc.]

Environment / dependencies:
    - Python version: [e.g., 3.11, if relevant]
    - Dependencies file: [requirements.txt / pyproject.toml / environment.yml]
    - External services: [Google Drive, Gmail API, OpenAI API, etc., if relevant]

How to run:
    python scripts/[00_short_name.py]

Notes:
    - [Known limitations, fragile steps, manual dependencies, or future improvements.]
"""

import logging
from pathlib import Path

# Use module-level logging so this file works both as a script and as an imported module.
# Larger pipelines can control this module's logs without editing this file.
LOG = logging.getLogger(__name__)

# All paths should be relative to the project root.
# Avoid hard-coded local paths such as C:/Users/... or /Users/name/...
PROJECT_ROOT = Path(__file__).resolve().parents[1]

LOG_FORMAT = "%(levelname)s:%(name)s:%(message)s"

# Stable configuration constants belong near the top.
# Use named constants instead of unexplained "magic numbers."
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30

INPUT_PATH = PROJECT_ROOT / "[relative/input/path]"
OUTPUT_PATH = PROJECT_ROOT / "[relative/output/path]"


def configure_logging() -> None:
    """Configure readable command-line logs."""
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def validate_inputs() -> None:
    """Validate required files, folders, settings, or arguments before doing work."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Missing input: {INPUT_PATH}")


def run_task() -> None:
    """Run the main task.

    Replace this placeholder with project-specific logic.
    Keep side effects explicit and documented in the file header.
    """
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    LOG.info("Running task")
    LOG.info("Input path: %s", INPUT_PATH)
    LOG.info("Output path: %s", OUTPUT_PATH)

    # TODO: Replace with actual task logic.


def main() -> None:
    """Configure, validate, and run the script."""
    configure_logging()
    validate_inputs()
    run_task()


# The main guard prevents this script from running accidentally when imported.
if __name__ == "__main__":
    main()
