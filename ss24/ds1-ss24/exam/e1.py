import os
from os.path import join
import pandas as pd
import re

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


def deduplicate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    original_length = len(df)
    df_deduped = df.drop_duplicates()
    rows_removed = original_length - len(df_deduped)
    print(f"Rows removed due to deduplication: {rows_removed}")
    return df_deduped


def process_cale_file(path: str):
    df = pd.read_excel(
        path,
        sheet_name="Verkaufsliste",
        skiprows=[0, 1],
        usecols=list(CALE_COLS.keys()),
        parse_dates=["Kaufdatum Lokal"],
        date_format="%d.%m.%Y %H:%M:%S",
        decimal=".",
    ).rename(columns=CALE_COLS)
    df["machine_ID"] = pd.to_numeric(
        df["machine_ID"].str.replace("PA", ""),
        errors="coerce",
    ).replace(0, 1)
    df = df.drop(df.loc[df["machine_ID"] == 999].index)
    df["category"] = "machine"
    return df


def process_parkster_file(path: str):
    df = pd.read_excel(
        path,
        sheet_name="Göttingen",
        usecols=list(PARKSTER_COLS.keys()),
        parse_dates=["Start"],
        date_format="%Y-%m-%d %H:%M:%S",
        decimal=",",
        dtype={
            "Parkgebühren inkl. MwSt. in EUR": "float64",
            "Zonencode": "int64",
        },
    ).rename(columns=PARKSTER_COLS)
    df["category"] = "app"
    return df


def load_psa_latlong(path: str):
    df = pd.read_csv(path).rename(columns={"PSA": "machine_ID"})
    df["machine_ID"] = pd.to_numeric(
        df["machine_ID"], downcast="integer", errors="coerce"
    )
    df.dropna(subset=["machine_ID"], inplace=True)
    df["machine_ID"] = df["machine_ID"].astype(int)
    df.set_index("machine_ID", inplace=True)
    return df


def load_parkzones_latlong(path: str):
    return pd.read_csv(path, usecols=["latitude", "longitude", "Zonencode"]).rename(
        columns={"Zonencode": "zone"}
    )


def process_excel_files(prefix: str) -> pd.DataFrame:
    files = [
        f for f in os.listdir(DATA_DIR) if f.startswith(prefix) and f.endswith(".xlsx")
    ]
    dfs = []

    for file in files:
        path = join(DATA_DIR, file)
        print(f"Loading {path}")
        df = (
            process_cale_file(path)
            if prefix.startswith("Cale")
            else process_parkster_file(path)
        )
        dfs.append(df)

    return deduplicate_dataframe(pd.concat(dfs, ignore_index=True))


def load_sales_data(prefix: str):
    print(f"Processing {prefix} data")
    df = process_excel_files(prefix)
    print(f"Done with {prefix} data")
    df.info()
    return df


def merge_and_format_data(
    cale_df: pd.DataFrame,
    parkster_df: pd.DataFrame,
    parkzones_latlong_df: pd.DataFrame,
    psa_latlong_df: pd.DataFrame,
) -> pd.DataFrame:
    cale_merged = pd.merge(
        cale_df,
        psa_latlong_df,
        on="machine_ID",
        how="left",
    ).rename(
        columns={
            "latitude": "latitude_machine",
            "longitude": "longitude_machine",
            "location": "street",
        }
    )

    combined_df = pd.concat([cale_merged, parkster_df], ignore_index=True)

    # Merge with parkzones_latlong
    final_df = pd.merge(combined_df, parkzones_latlong_df, on="zone", how="left")

    final_df = final_df.rename(
        columns={"latitude": "latitude_zone", "longitude": "longitude_zone"}
    )

    # final_df = (
    #     final_df[
    #         [
    #             "time",
    #             "machine_ID",
    #             "fee",
    #             "category",
    #             "street",
    #             "latitude_machine",
    #             "longitude_machine",
    #             "zone",
    #             "latitude_zone",
    #             "longitude_zone",
    #         ]
    #     ]
    # )

    return final_df


def main():
    # # Stage 1: Load initial excel files
    cale_df = load_sales_data("Cale")
    parkster_df = load_sales_data("Parkster")

    # # Stage 2: Load and transform additional data
    parkzones_latlong_df = load_parkzones_latlong(
        join(DATA_DIR, "parkzones_latlong.csv")
    )
    parkzones_latlong_df.info()

    psa_latlong_df = load_psa_latlong(join(DATA_DIR, "psa_latlong.csv"))

    # # Print summary
    print("\nData Processing Summary:")
    print(f"Cale DataFrame shape: {cale_df.shape}")
    cale_df.info()
    print(f"Parkster DataFrame shape: {parkster_df.shape}")
    parkster_df.info()
    print(f"Parkzones LatLong DataFrame shape: {parkzones_latlong_df.shape}")
    parkzones_latlong_df.info()
    print(f"PSA LatLong DataFrame shape: {psa_latlong_df.shape}")
    psa_latlong_df.info()

    # # Stage 3: Merge and format data
    final_df = merge_and_format_data(
        cale_df, parkster_df, parkzones_latlong_df, psa_latlong_df
    )

    print("\nFinal DataFrame:")
    final_df.info()
    final_df.to_csv("out/final_df.csv", index=False)

    print("Reference DataFrame:")
    clean_df = pd.read_csv(
        "data/clean_dataframe.csv",
        parse_dates=["time"],
        index_col="time",
        dtype={
            "machine_ID": "Int64",
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

    fdf = pd.read_csv(
        "out/final_df.csv",
        parse_dates=["time"],
        index_col="time",
        dtype={
            "machine_ID": "Int64",
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
    fdf.info()

    print(f"Equal: {final_df.equals(clean_df)}")


if __name__ == "__main__":
    main()
