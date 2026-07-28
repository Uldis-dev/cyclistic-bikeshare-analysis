import os
import glob
import pandas as pd

def inspect_raw_data(data_dir: str):
    """
    Iterates through all monthly CSV files in the raw data directory,
    verifying row counts, column structure, data types, and missing values.
    """
    # Find all CSV files in the target directory
    csv_files = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    
    if not csv_files:
        print(f"[ERROR] No CSV files found in path: {data_dir}")
        return

    print(f"Found {len(csv_files)} CSV files in '{data_dir}'. Starting inspection...\n")
    print("=" * 80)

    total_rows_all_files = 0
    schema_reference = None
    all_schemas_match = True

    summary_list = []

    for file_path in csv_files:
        filename = os.path.basename(file_path)
        
        # Read a small sample first to check column structure
        df_sample = pd.read_csv(file_path, nrows=5)
        current_columns = list(df_sample.columns)

        # Set reference schema from the first file
        if schema_reference is None:
            schema_reference = current_columns
        elif current_columns != schema_reference:
            all_schemas_match = False
            print(f"[WARNING] Column mismatch found in file: {filename}")

        # Read complete file for row counts and missing value analysis
        df = pd.read_csv(file_path, low_memory=False)
        file_rows = len(df)
        total_rows_all_files += file_rows

        # Track missing values per column
        null_counts = df.isnull().sum()
        cols_with_nulls = null_counts[null_counts > 0].to_dict()

        summary_list.append({
            "File": filename,
            "Rows": file_rows,
            "Columns": len(df.columns),
            "Null_Columns_Count": len(cols_with_nulls)
        })

        print(f"File: {filename}")
        print(f"  - Total Rows: {file_rows:,}")
        print(f"  - Total Columns: {len(df.columns)}")
        if cols_with_nulls:
            print("  - Missing Values per Column:")
            for col, count in cols_with_nulls.items():
                pct = (count / file_rows) * 100
                print(f"      * {col}: {count:,} ({pct:.2f}%)")
        else:
            print("  - Missing Values: None")
        print("-" * 80)

    # Final summary output
    print("\n" + "=" * 80)
    print("INSPECTION SUMMARY")
    print("=" * 80)
    print(f"Total Files Processed: {len(csv_files)}")
    print(f"Total Combined Rows:   {total_rows_all_files:,}")
    print(f"Schema Consistency:    {'PASS (All file columns match)' if all_schemas_match else 'FAIL (Column mismatches detected)'}")
    print("=" * 80)

if __name__ == "__main__":
    # Path to your raw data directory
    RAW_DATA_PATH = os.path.join("C:", os.sep, "DEV", "cyclistic-bikeshare-analysis", "data", "raw")
    inspect_raw_data(RAW_DATA_PATH)