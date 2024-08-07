import os
from os.path import join
import pandas as pd
import re

import pandas as pd

DATA_DIR = "data"
CALE_COLS = {
    "Automat - Automaten ID": "machine_ID",
    "Kaufdatum Lokal": "time",
    "Betrag": "fee",
}
PARKSTER_COLS = {
    "Start": "time",
    "Parkgebühren inkl. MwSt. in EUR": "fee",
    "Zonencode": "zone",
}


def load_cale(path: str):
    df = pd.read_excel(
        path,
        sheet_name="Verkaufsliste",
        skiprows=[0, 1],
        usecols=list(CALE_COLS.keys()),
        parse_dates=["Kaufdatum Lokal"],
        date_format="%d.%m.%Y %H:%M:%S",
    ).rename(columns=CALE_COLS)

    df["category"] = "machine"
    df["machine_ID"] = pd.to_numeric(
        df["machine_ID"].astype(str).str.replace("PA", ""), errors="coerce"
    )

    df["machine_ID"].replace(0, 1, inplace=True)
    df.drop(df.loc[df["machine_ID"] == 999].index, inplace=True)
    return df


def load_parkster(path: str):
    return pd.read_excel(
        path,
        sheet_name="Göttingen",
        usecols=list(PARKSTER_COLS.keys()),
        parse_dates=["time"],
        date_format="%Y-%m-%d %H:%M:%S",
    ).rename(columns=PARKSTER_COLS)


def load_psa_latlong(path: str):
    df = pd.read_csv(path).rename(columns={"PSA": "machine_ID"})
    df["machine_ID"] = pd.to_numeric(df["machine_ID"], downcast="integer", errors="coerce")
    df.dropna(subset=["machine_ID"], inplace=True)
    df["machine_ID"] = df["machine_ID"].astype(int)
    df.set_index("machine_ID", inplace=True)
    return df


def process_excel_files(prefix: str) -> pd.DataFrame:
    files = [
        f for f in os.listdir(DATA_DIR) if f.startswith(prefix) and f.endswith(".xlsx")
    ]
    dfs = []

    for file in files:
        path = join(DATA_DIR, file)
        print(f"Loading {path}")
        df = load_cale(path) if prefix.startswith("Cale") else load_parkster(path)
        dfs.append(df)

    return deduplicate_dataframe(pd.concat(dfs, ignore_index=True))


def deduplicate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    original_length = len(df)
    df_deduped = df.drop_duplicates()
    rows_removed = original_length - len(df_deduped)
    print(f"Rows removed due to deduplication: {rows_removed}")
    return df_deduped


def load_cached_data_file(prefix):
    csv_path = f"out/{prefix.lower()}_combined.csv"
    if os.path.exists(csv_path):
        print(f"Loading existing {csv_path}")
        df = pd.read_csv(csv_path)
    else:
        print(f"Processing {prefix} data")
        df = process_excel_files(prefix)
        df.to_csv(csv_path, index=False)
        print(f"Saved processed data to {csv_path}")
    return df


def merge_and_format_data(cale_df, parkster_df, parkzones_latlong_df, psa_latlong_df):
    # Merge Cale data with psa_latlong
    psa_latlong_df.info()
    cale_merged = pd.merge(
        cale_df,
        psa_latlong_df,
        on="machine_ID",
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
    parkzones_latlong_df = parkzones_latlong_df.rename(columns={"Zonencode": "zone"})
    final_df = pd.merge(combined_df, parkzones_latlong_df, on="zone", how="left")

    # Use dayfirst=True to correctly parse the German date format
    # final_df["time"] = pd.to_datetime(final_df["time"], dayfirst=True)
    final_df["time"] = pd.to_datetime(final_df["time"], format="mixed", dayfirst=True)

    final_df = final_df.rename(
        columns={"latitude": "latitude_zone", "longitude": "longitude_zone"}
    )

    # Select and reorder columns
    final_df = final_df[
        [
            "time",
            "machine_ID",
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
    # final_df["machine_ID"] = pd.to_numeric(
    #     final_df["machine_ID"], errors="coerce"
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
    # # Stage 1: Load initial excel files
    # cale_df = load_or_process_data("Cale-", transform_cale_data)
    # parkster_df = load_or_process_data("Parkster-")

    # # Stage 2: Load and transform additional data
    # parkzones_latlong_df = pd.read_csv(join(DATA_DIR, "parkzones_latlong.csv"))
    # parkzones_latlong_df = deduplicate_dataframe(parkzones_latlong_df)

    # psa_latlong_df = pd.read_csv(join(DATA_DIR, "psa_latlong.csv"))
    # psa_latlong_df = transform_psa_latlong_data(psa_latlong_df)
    # psa_latlong_df.to_csv("out/filtered_psa_latlong.csv", index=False)

    # # Print summary
    # print("\nData Processing Summary:")
    # print(f"Cale DataFrame shape: {cale_df.shape}")
    # print(f"Parkster DataFrame shape: {parkster_df.shape}")
    # print(f"Parkzones LatLong DataFrame shape: {parkzones_latlong_df.shape}")
    # print(f"PSA LatLong DataFrame shape: {psa_latlong_df.shape}")

    # # Stage 3: Merge and format data
    # final_df = merge_and_format_data(
    #     cale_df, parkster_df, parkzones_latlong_df, psa_latlong_df
    # )

    # print("Reference DataFrame:")
    # clean_df = pd.read_csv(
    #     "data/clean_dataframe.csv",
    #     parse_dates=["time"],
    #     index_col="time",
    #     dtype={
    #         "machine_ID": "Int64",
    #         "fee": "float64",
    #         "category": "object",
    #         "street": "object",
    #         "latitude_machine": "float64",
    #         "longitude_machine": "float64",
    #         "zone": "int64",
    #         "latitude_zone": "float64",
    #         "longitude_zone": "float64",
    #     },
    # ).sort_index()
    # clean_df.info()

    # print("\nFinal DataFrame:")
    # final_df.info()

    # print(f"Equal: {final_df.equals(clean_df)}")

    # final_df.to_csv(join("out", "my_clean_dataframe.csv"))
    parkster = process_excel_files("Parkster-")
    parkster.info()
    cale = process_excel_files("Cale-")
    cale.info()
    df = load_psa_latlong(join(DATA_DIR, "psa_latlong.csv"))
    df.info()
    print(df)


if __name__ == "__main__":
    main()
