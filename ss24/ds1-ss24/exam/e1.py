# import os
# from os.path import join
# import pandas as pd
# import re

# DATA_DIR = "data"
# ID_COLUMN_ORIG = "Automat - Automaten ID"
# ID_COLUMN = "pa_id"


# # File loading functions
# def load_cale(path):
#     return pd.read_excel(path, "Verkaufsliste", skiprows=range(0, 2))


# def load_parkster(path):
#     return pd.read_excel(path, "Göttingen")


# def process_excel_files(directory, prefix):
#     files = [
#         f
#         for f in os.listdir(directory)
#         if f.startswith(prefix) and f.endswith(".xlsx")
#     ]
#     dfs = []

#     for file in files:
#         path = join(directory, file)
#         print(f"Loading {path}")
#         df = load_cale(path) if prefix == "Cale-" else load_parkster(path)
#         df["Month"] = file.split()[-2]
#         dfs.append(df)

#     if dfs:
#         return pd.concat(dfs, ignore_index=True)
#     else:
#         print(f"No valid data found for {prefix} files.")
#         return pd.DataFrame()


# def is_valid_id(id_str):
#     return bool(re.match(r"^PA\d+$", id_str))


# def strip_pa(val: str) -> str:
#     return val.lstrip("PA")


# def check_id_validity(df, column):
#     invalid_ids = df[~df[column].apply(is_valid_id)]
#     if invalid_ids.empty:
#         print("All IDs conform to the pattern 'PA' followed by digits.")
#     else:
#         print(
#             f"Warning: Found {len(invalid_ids)} IDs that do not conform to the expected pattern:"
#         )
#         print(invalid_ids[column].tolist())


# def deduplicate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
#     original_length = len(df)
#     df_deduped = df.drop_duplicates()
#     rows_removed = original_length - len(df_deduped)
#     print(f"Rows removed due to deduplication: {rows_removed}")
#     return df_deduped


# def process_data(
#     cale_df: pd.DataFrame,
#     parkster_df: pd.DataFrame,
#     parkzones_latlong_df: pd.DataFrame,
#     psa_latlong_df: pd.DataFrame,
# ):
#     print(f"Original Cale DataFrame shape: {cale_df.shape}")
#     print(f"Original Parkster DataFrame shape: {parkster_df.shape}")

#     cale_df = cale_df.rename(columns={ID_COLUMN_ORIG: ID_COLUMN})
#     cale_df.pa_id = cale_df.pa_id.map(strip_pa)
#     cale_df.pa_id = pd.to_numeric(cale_df.pa_id, errors="coerce")

#     # Change 0's to 1's
#     cale_df[ID_COLUMN] = cale_df[ID_COLUMN].replace(0, 1)
#     # Filter out 999's
#     cale_df = cale_df[cale_df[ID_COLUMN] != 999]

#     # Deduplicate dataframes
#     cale_df = deduplicate_dataframe(cale_df)
#     parkster_df = deduplicate_dataframe(parkster_df)
#     parkzones_latlong_df = deduplicate_dataframe(parkzones_latlong_df)
#     parkzones_latlong_df = deduplicate_dataframe(psa_latlong_df)

#     print(f"Final Cale DataFrame shape: {cale_df.shape}")
#     print(f"Final Parkster DataFrame shape: {parkster_df.shape}")

#     original_row_count = len(psa_latlong_df)

#     # Convert PSA column to numeric, coercing errors to NaN
#     psa_latlong_df["PSA"] = pd.to_numeric(
#         psa_latlong_df["PSA"], errors="coerce"
#     )

#     # Create a boolean mask for rows to keep
#     mask = psa_latlong_df["PSA"].notna() & psa_latlong_df["PSA"].apply(
#         lambda x: x.is_integer()
#     )

#     # Get the filtered out rows
#     filtered_out_rows = psa_latlong_df[~mask]

#     # Apply the mask to keep only valid rows
#     psa_latlong_df = psa_latlong_df[mask]

#     # Reset the index if needed
#     psa_latlong_df = psa_latlong_df.reset_index(drop=True)

#     # Calculate how many rows were filtered out
#     filtered_out_count = original_row_count - len(psa_latlong_df)

#     # Print the number of rows filtered out
#     print(f"Number of rows filtered out: {filtered_out_count}")

#     # Print the PSA values of the filtered out rows
#     print("PSA values of filtered out rows:")
#     print(filtered_out_rows["PSA"].tolist())

#     print("\nFirst few rows of the filtered DataFrame:")
#     print(psa_latlong_df.head())

#     psa_latlong_df.to_csv("filtered_psa_latlong.csv", index=False)

#     return cale_df, parkster_df


# if __name__ == "__main__":
#     cale_df = process_excel_files(DATA_DIR, "Cale-")
#     parkster_df = process_excel_files(DATA_DIR, "Parkster-")
#     cale_df.info()
#     parkster_df.info()
#     # Load and process data
#     # cale_df = pd.read_csv("cale_combined.csv")
#     # check_id_validity(cale_df, ID_COLUMN)
#     # parkster_df = pd.read_csv("parkster_combined.csv")
#     # parkzones_latlong_df = pd.read_csv(join(DATA_DIR, "parkzones_latlong.csv"))
#     # psa_latlong_df = pd.read_csv(join(DATA_DIR, "psa_latlong.csv"))

#     # cale_df, parkster_df = process_data(
#         # cale_df, parkster_df, parkzones_latlong_df, psa_latlong_df
#     # )

#     # cale_df.to_csv("cale_combined_updated.csv", index=False)
#     # # parkster_df.to_csv("parkster_combined_updated.csv", index=False)

#     # print("1.1: Data processing completed and results saved.")

#     # 1.2 Merging and Formating
#     # merge psa_latlong and cale

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

def process_excel_files(directory, prefix):
    files = [f for f in os.listdir(directory) if f.startswith(prefix) and f.endswith(".xlsx")]
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

def deduplicate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    original_length = len(df)
    df_deduped = df.drop_duplicates()
    rows_removed = original_length - len(df_deduped)
    print(f"Rows removed due to deduplication: {rows_removed}")
    return df_deduped

def transform_cale_data(df):
    df = df.rename(columns={ID_COLUMN_ORIG: ID_COLUMN})
    df[ID_COLUMN] = pd.to_numeric(df[ID_COLUMN].astype(str).str.replace('PA', ''), errors='coerce')
    df[ID_COLUMN] = df[ID_COLUMN].replace(0, 1)
    df = df[df[ID_COLUMN] != 999]
    return deduplicate_dataframe(df)

def transform_psa_latlong_data(df):
    df["PSA"] = pd.to_numeric(df["PSA"], errors="coerce")
    mask = df["PSA"].notna() & df["PSA"].apply(lambda x: x.is_integer())
    filtered_out_rows = df[~mask]
    df = df[mask].reset_index(drop=True)
    print(f"Number of rows filtered out: {len(filtered_out_rows)}")
    print("PSA values of filtered out rows:")
    print(filtered_out_rows["PSA"].tolist())
    return df

def load_or_process_data(prefix, transform_func=None):
    csv_path = f"{prefix.lower()}_combined.csv"
    if os.path.exists(csv_path):
        print(f"Loading existing {csv_path}")
        df = pd.read_csv(csv_path)
    else:
        print(f"Processing {prefix} data")
        df = process_excel_files(DATA_DIR, prefix)
        if transform_func:
            df = transform_func(df)
        df.to_csv(csv_path, index=False)
        print(f"Saved processed data to {csv_path}")
    return df

def merge_and_format_data(cale_df, parkster_df, parkzones_latlong_df, psa_latlong_df):
    # Prepare Cale data
    cale_df = cale_df.rename(columns={
        ID_COLUMN: 'machine_ID',
        'Kaufdatum Lokal': 'time',
        'Betrag': 'fee',
    })
    # Use dayfirst=True to correctly parse the German date format
    cale_df['time'] = pd.to_datetime(cale_df['time'], dayfirst=True)
    # cale_df = cale_df[['time', 'machine_ID', 'fee', 'category']]
    cale_df = cale_df[['time', 'machine_ID', 'fee']]
    cale_df["category"] = "machine"

    # Prepare Parkster data
    parkster_df = parkster_df.rename(columns={
        'Start': 'time',
        'Parkgebühren inkl. MwSt. in EUR': 'fee',
        'Zonencode': 'zone'
    })
    print("hi")
    parkster_df.info()

    parkster_df['time'] = pd.to_datetime(parkster_df['time'], errors='coerce')
    parkster_df['category'] = 'app'
    parkster_df = parkster_df[['time', 'fee', 'category', 'Parkzone']]

    # Merge Cale data with psa_latlong
    cale_merged = pd.merge(cale_df, psa_latlong_df, left_on='machine_ID', right_on='PSA', how='left')
    cale_merged.info()
    cale_merged = cale_merged.rename(columns={
        'latitude': 'latitude_machine',
        'longitude': 'longitude_machine',
        'location': 'street',
        # 'Zone': 'zone'
    })

    # Merge both datasets
    combined_df = pd.concat([cale_merged, parkster_df], ignore_index=True)
    combined_df.info()

    # Merge with parkzones_latlong
    parkzones_latlong_df = parkzones_latlong_df.rename(columns={"Zonencode": "zone"})
    final_df = pd.merge(combined_df, parkzones_latlong_df, on='zone', how='left')

    final_df = final_df.rename(columns={
        'Latitude': 'latitude_zone',
        'Longitude': 'longitude_zone'
    })

    # Select and reorder columns
    final_df = final_df[[
        'time', 'machine_ID', 'fee', 'category', 'street', 
        'latitude_machine', 'longitude_machine', 'zone',
        'latitude_zone', 'longitude_zone'
    ]]

    # Set time as index and sort
    final_df.set_index('time', inplace=True)
    final_df.sort_index(inplace=True)

    # Ensure correct data types
    final_df['machine_ID'] = pd.to_numeric(final_df['machine_ID'], errors='coerce').astype('Int64')
    final_df['fee'] = final_df['fee'].astype('float64')
    final_df['zone'] = final_df['zone'].astype('int64')
    float_columns = ['latitude_machine', 'longitude_machine', 'latitude_zone', 'longitude_zone']
    final_df[float_columns] = final_df[float_columns].astype('float64')

    return final_df


def main():
    # Stage 1: Load initial excel files
    cale_df = load_or_process_data("Cale-", transform_cale_data)
    parkster_df = load_or_process_data("Parkster-")

    # Stage 2: Load and transform additional data
    parkzones_latlong_df = pd.read_csv(join(DATA_DIR, "parkzones_latlong.csv"))
    parkzones_latlong_df = deduplicate_dataframe(parkzones_latlong_df)

    psa_latlong_df = pd.read_csv(join(DATA_DIR, "psa_latlong.csv"))
    psa_latlong_df = transform_psa_latlong_data(psa_latlong_df)
    psa_latlong_df.to_csv("filtered_psa_latlong.csv", index=False)

    # Print summary
    print("\nData Processing Summary:")
    print(f"Cale DataFrame shape: {cale_df.shape}")
    print(f"Parkster DataFrame shape: {parkster_df.shape}")
    print(f"Parkzones LatLong DataFrame shape: {parkzones_latlong_df.shape}")
    print(f"PSA LatLong DataFrame shape: {psa_latlong_df.shape}")

    clean = pd.read_csv('data/clean_dataframe.csv', parse_dates=['time'], index_col='time', dtype={'machine_ID': 'Int64', 
                                                                           'fee': 'float64', 
                                                                           'category': 'object', 
                                                                           'street': 'object', 
                                                                           'latitude_machine': 'float64', 
                                                                           'longitude_machine': 'float64', 
                                                                           'zone': 'int64', 
                                                                           'latitude_zone': 'float64', 
                                                                           'longitude_zone': 'float64'}).sort_index()
    clean.info()

        # Stage 3: Merge and format data
    final_df = merge_and_format_data(cale_df, parkster_df, parkzones_latlong_df, psa_latlong_df)

    # Save the final DataFrame
    final_df.to_csv(join(DATA_DIR, "clean_dataframe.csv"))

    # Print summary
    print("\nFinal DataFrame Info:")
    final_df.info()

if __name__ == "__main__":
    main()