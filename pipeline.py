"""
Data Processing Pipeline - CLI Template
DS 3500 - MP1
Usage:
python pipeline.py --input data.csv --output clean.csv
python pipeline.py --input data.csv --output results.json --format json --
verbose
"""

import argparse
import logging
import sys

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Data Processing Pipeline"
    )

    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to the input file"
    )

    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to the output file"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to the YAML configuration file"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()
    return args


def main():
    """Main pipeline function."""
    args = parse_arguments()

    setup_logging(args.verbose)

    logger.debug(
        f"Arguments parsed: input={args.input}, output={args.output}, config={args.config}"
    )

    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]

    rows_before_validation = len(data)

    try:
        data = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)

    rows_after_validation = len(data)

    logger.info(
        f"Validation complete: {rows_before_validation} -> {rows_after_validation} rows"
    )

    df_original = data.copy()

    try:
        df_processed = process_data(data, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(df_original, df_processed)

    logger.info(
        f"Processing complete: {report['rows_before']} → {report['rows_after']} rows"
    )

    save_data(df_processed, args.output)
    logger.info(f"Saved cleaned data to {args.output}")

    print(report)


if __name__ == "__main__":
    main()