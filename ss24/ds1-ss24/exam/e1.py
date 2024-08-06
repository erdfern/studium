import os
from os.path import join
import pandas as pd
import re

DATA_DIR = "data"
ID_COLUMN_ORIG = "Automat - Automaten ID"
ID_COLUMN = "machine_id"
# machine_id,Zahleinheit - Name,Knoten,Kaufdatum Lokal,Betrag,Artikelname,Artikel ID,Tarifpaket - Name,Maskierter PAN,Transaktionsreferenz,Ticket Nummer,month
CALE_COLS = {
    "Automat - Automaten ID": "machine_ID",
    "Knoten": "node",
    "Kaufdatum Lokal": "time",
    "Betrag": "fee",
}
# Parkzone,Erstellt,Start,Stopp,Parkgebühren inkl. MwSt. in EUR,Status,Parkscheinart,Zonencode,Eigentümercode,month
# TODO verify that Parkzone and Zonencode are identical
PARKSTER_COLS = {
    "Parkzone": "zone",
    "Start": "time",
    "Parkgebühren inkl. MwSt. in EUR": "fee",
}


# File loading functions
def load_cale(path):
    return transform_cale_data(
        pd.read_excel(path, "Verkaufsliste", skiprows=range(0, 2))
    )


def load_parkster(path):
    return pd.read_excel(path, "Göttingen")


def process_excel_files(directory, prefix):
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
        df["month"] = file.split()[-2]
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


def transform_cale_data(df: pd.DataFrame):
    df = df.rename(columns=CALE_COLS)
    # cale_df = cale_df[['time', 'machine_id', 'fee', 'category']]
    df = df[["time", "machine_id", "fee"]]
    df["category"] = "machine"
    df["machine_id"] = pd.to_numeric(
        df["machine_id"].astype(str).str.replace("PA", ""), errors="coerce"
    )
    df["machine_id"] = df["machine_id"].replace(0, 1)
    df = df[df["machine_id"] != 999]
    return deduplicate_dataframe(df)


def transform_psa_latlong_data(df):
    df["PSA"] = pd.to_numeric(df["PSA"], errors="coerce")
    mask = df["PSA"].notna() & df["PSA"].apply(lambda x: x.is_integer())
    filtered_out_rows = df[~mask]
    df = df[mask].reset_index(drop=True)
    print(f"Number of rows filtered out: {len(filtered_out_rows)}")
    return df


def load_or_process_data(prefix, transform_func=None):
    csv_path = f"out/{prefix.lower()}_combined.csv"
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


def merge_and_format_data(
    cale_df, parkster_df, parkzones_latlong_df, psa_latlong_df
):
    # Prepare Parkster data
    parkster_df = parkster_df.rename(columns=PARKSTER_COLS)

    # parkster_df["time"] = pd.to_datetime(parkster_df["time"], errors="coerce")
    parkster_df["category"] = "app"
    parkster_df = parkster_df[["time", "fee", "category", "zone"]]

    # Merge Cale data with psa_latlong
    psa_latlong_df = psa_latlong_df.rename(columns={"PSA": "machine_id"})
    psa_latlong_df.info()
    cale_merged = pd.merge(
        cale_df,
        psa_latlong_df,
        on="machine_id",
        how="left",
    )
    print("cale_merged")
    cale_merged.info()
    cale_merged = cale_merged.rename(
        columns={
            "latitude": "latitude_machine",
            "longitude": "longitude_machine",
            "location": "street",
        }
    )

    # Merge both datasets
    combined_df = pd.concat([cale_merged, parkster_df], ignore_index=True)
    combined_df.info()

    # Merge with parkzones_latlong
    parkzones_latlong_df = parkzones_latlong_df.rename(
        columns={"Zonencode": "zone"}
    )
    final_df = pd.merge(
        combined_df, parkzones_latlong_df, on="zone", how="left"
    )

    # Use dayfirst=True to correctly parse the German date format
    # final_df["time"] = pd.to_datetime(final_df["time"], dayfirst=True)
    final_df["time"] = pd.to_datetime(final_df["time"], dayfirst=False)

    final_df = final_df.rename(
        columns={"latitude": "latitude_zone", "longitude": "longitude_zone"}
    )

    # Select and reorder columns
    final_df = final_df[
        [
            "time",
            "machine_id",
            "fee",
            "category",
            "street",
            "latitude_machine",
            "longitude_machine",
            "zone",
            "latitude_zone",
            "longitude_zone",
        ]
    ]

    # Set time as index and sort
    final_df.set_index("time", inplace=True)
    final_df.sort_index(inplace=True)

    # Ensure correct data types
    # final_df["machine_id"] = pd.to_numeric(
    #     final_df["machine_id"], errors="coerce"
    # ).astype("Int64")
    # final_df["fee"] = final_df["fee"].astype("float64")
    # final_df["zone"] = final_df["zone"].astype("int64")
    # float_columns = [
    # "latitude_machine",
    # "longitude_machine",
    # "latitude_zone",
    # "longitude_zone",
    # ]
    # final_df[float_columns] = final_df[float_columns].astype("float64")

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
    psa_latlong_df.to_csv("out/filtered_psa_latlong.csv", index=False)

    # Print summary
    print("\nData Processing Summary:")
    print(f"Cale DataFrame shape: {cale_df.shape}")
    print(f"Parkster DataFrame shape: {parkster_df.shape}")
    print(f"Parkzones LatLong DataFrame shape: {parkzones_latlong_df.shape}")
    print(f"PSA LatLong DataFrame shape: {psa_latlong_df.shape}")

    # Stage 3: Merge and format data
    final_df = merge_and_format_data(
        cale_df, parkster_df, parkzones_latlong_df, psa_latlong_df
    )

    print("Reference DataFrame:")
    clean_df = pd.read_csv(
        "data/clean_dataframe.csv",
        parse_dates=["time"],
        index_col="time",
        dtype={
            "machine_id": "Int64",
            "fee": "float64",
            "category": "object",
            "street": "object",
            "latitude_machine": "float64",
            "longitude_machine": "float64",
            "zone": "int64",
            "latitude_zone": "float64",
            "longitude_zone": "float64",
        },
    ).sort_index()
    clean_df.info()

    print("\nFinal DataFrame:")
    final_df.info()

    print(f"Equal: {final_df.equals(clean_df)}")

    final_df.to_csv(join("out", "my_clean_dataframe.csv"))


if __name__ == "__main__":
    main()
