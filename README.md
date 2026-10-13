# MP1: Data Processing Pipeline

This project is an end-to-end command-line data pipeline built for DS 3500. The pipeline loads a CSV file, validates it against a configuration file, cleans the data, and saves the final result to a new CSV file. Data moves through four stages: loading, validation, processing, and output, each handled by its own module inside the `src/` package. `pipeline.py` coordinates these stages but does not implement any of the logic itself.

The `src/data_loaders.py` module reads CSV, JSON, and YAML files and returns them as Python objects or DataFrames. `src/data_validator.py` checks that required columns exist and converts configured numeric columns, removing rows with invalid values. `src/data_processor.py` removes duplicate rows, handles missing values, and removes outliers using the IQR or Z-score method, all controlled through `config/config.yaml`. `src/data_output.py` saves the final cleaned DataFrame to the specified output path, creating the output directory if needed. `src/utils.py` contains shared logging setup and input-file validation used across the pipeline.

To run the pipeline with the provided sample data:

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

Example output:

```text
22:56:56 INFO     src.utils — Input file validated: fixtures/sample_data.csv
22:56:56 INFO     src.utils — Input file validated: config/config.yaml
22:56:56 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
22:56:56 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
22:56:56 INFO     __main__ — Validation complete: 100 -> 98 rows
22:56:56 INFO     __main__ — Processing complete: 98 → 92 rows
22:56:56 INFO     __main__ — Saved cleaned data to output/clean.csv
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
```
