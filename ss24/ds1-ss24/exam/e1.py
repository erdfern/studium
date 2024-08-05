import os
from os.path import join
import pandas as pd
import re

DATA_DIR = "data"
ID_COLUMN_ORIG = "Automat - Automaten ID"
ID_COLUMN = "pa_id"


# File loading functions
def load_cale(path):
    return pd.read_excel(path, "Verkaufsliste", skiprows=range(0, 2))


def load_parkster(path):
    return pd.read_excel(path, "Göttingen")


def process_excel_files(directory, prefix, sheet_name):
    files = [
        f
        for f in os.listdir(directory)
        if f.startswith(prefix) and f.endswith(".xlsx")
    ]
    dfs = []

    for file in files:
        path = join(directory, file)
        print(f"Loading {path}")
        df = load_cale(path) if prefix == "Cale-" else load_parkster(path)
        df["Month"] = file.split()[-2]
        dfs.append(df)

    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        print(f"No valid data found for {prefix} files.")
        return pd.DataFrame()


def is_valid_id(id_str):
    return bool(re.match(r"^PA\d+$", id_str))


def strip_pa(val: str) -> str:
    return val.lstrip("PA")


def check_id_validity(df, column):
    invalid_ids = df[~df[column].apply(is_valid_id)]
    if invalid_ids.empty:
        print("All IDs conform to the pattern 'PA' followed by digits.")
    else:
        print(
            f"Warning: Found {len(invalid_ids)} IDs that do not conform to the expected pattern:"
        )
        print(invalid_ids[column].tolist())


def deduplicate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    original_length = len(df)
    df_deduped = df.drop_duplicates()
    rows_removed = original_length - len(df_deduped)
    print(f"Rows removed due to deduplication: {rows_removed}")
    return df_deduped


def process_data(
    cale_df: pd.DataFrame,
    parkster_df: pd.DataFrame,
    parkzones_latlong_df: pd.DataFrame,
    psa_latlong_df: pd.DataFrame,
):
    print(f"Original Cale DataFrame shape: {cale_df.shape}")
    print(f"Original Parkster DataFrame shape: {parkster_df.shape}")

    cale_df = cale_df.rename(columns={ID_COLUMN_ORIG: ID_COLUMN})
    cale_df.pa_id = cale_df.pa_id.map(strip_pa)
    cale_df.pa_id = pd.to_numeric(cale_df.pa_id, errors="coerce")

    # Change 0's to 1's
    cale_df[ID_COLUMN] = cale_df[ID_COLUMN].replace(0, 1)
    # Filter out 999's
    cale_df = cale_df[cale_df[ID_COLUMN] != 999]

    # Deduplicate dataframes
    cale_df = deduplicate_dataframe(cale_df)
    parkster_df = deduplicate_dataframe(parkster_df)
    parkzones_latlong_df = deduplicate_dataframe(parkzones_latlong_df)
    parkzones_latlong_df = deduplicate_dataframe(psa_latlong_df)

    print(f"Final Cale DataFrame shape: {cale_df.shape}")
    print(f"Final Parkster DataFrame shape: {parkster_df.shape}")

    original_row_count = len(psa_latlong_df)

    # Convert PSA column to numeric, coercing errors to NaN
    psa_latlong_df["PSA"] = pd.to_numeric(
        psa_latlong_df["PSA"], errors="coerce"
    )

    # Create a boolean mask for rows to keep
    mask = psa_latlong_df["PSA"].notna() & psa_latlong_df["PSA"].apply(
        lambda x: x.is_integer()
    )

    # Get the filtered out rows
    filtered_out_rows = psa_latlong_df[~mask]

    # Apply the mask to keep only valid rows
    psa_latlong_df = psa_latlong_df[mask]

    # Reset the index if needed
    psa_latlong_df = psa_latlong_df.reset_index(drop=True)

    # Calculate how many rows were filtered out
    filtered_out_count = original_row_count - len(psa_latlong_df)

    # Print the number of rows filtered out
    print(f"Number of rows filtered out: {filtered_out_count}")

    # Print the PSA values of the filtered out rows
    print("PSA values of filtered out rows:")
    print(filtered_out_rows["PSA"].tolist())

    print("\nFirst few rows of the filtered DataFrame:")
    print(psa_latlong_df.head())

    psa_latlong_df.to_csv("filtered_psa_latlong.csv", index=False)

    return cale_df, parkster_df


if __name__ == "__main__":
    # Load and process data
    cale_df = pd.read_csv("cale_combined.csv")
    # check_id_validity(cale_df, ID_COLUMN)
    parkster_df = pd.read_csv("parkster_combined.csv")
    parkzones_latlong_df = pd.read_csv(join(DATA_DIR, "parkzones_latlong.csv"))
    psa_latlong_df = pd.read_csv(join(DATA_DIR, "psa_latlong.csv"))

    cale_df, parkster_df = process_data(
        cale_df, parkster_df, parkzones_latlong_df, psa_latlong_df
    )

    cale_df.to_csv("cale_combined_updated.csv", index=False)
    # # parkster_df.to_csv("parkster_combined_updated.csv", index=False)

    print("1.1: Data processing completed and results saved.")

    # 1.2 Merging and Formating
    # merge psa_latlong and cale
    cale_latlong_df = cale_df.merge(psa_latlong_df, how="left", on="pa_id")
    cale_latlong_df.info()

