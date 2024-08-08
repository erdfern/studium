import os
from os.path import join
import pandas as pd

DATA_DIR = "data"
PICKLE_DIR = "pickles"
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
    # df_deduped = df.drop_duplicates(keep="first")
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
    # df = df.drop_duplicates(["machine_ID"])
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
    """
    Loads and concatenates either Cale- or Parkster- excel sheets.
    """
    pickle_file = os.path.join(PICKLE_DIR, f"{prefix}_df")
    if os.path.exists(pickle_file):
        print(f"Loading DataFrame from {pickle_file}")
        return pd.read_pickle(pickle_file)

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

    # df = deduplicate_dataframe(pd.concat(dfs, ignore_index=True))
    df = pd.concat(dfs, ignore_index=True)
    df.to_pickle(pickle_file)
    return df


def merge_and_format_data(
    cale_df: pd.DataFrame,
    parkster_df: pd.DataFrame,
    parkzones_latlong_df: pd.DataFrame,
    psa_latlong_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    This function produces the final dataframe for exercise 1.2 by
    merging all the loaded data as specified.
    """
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

    print("Shapes after merging Cale and PSA LatLong:")
    print(f"Cale merged DataFrame shape: {cale_merged.shape}")

    combined_df = pd.concat([cale_merged, parkster_df], ignore_index=True)

    print("Shapes after concatenating Cale and Parkster:")
    print(f"Combined DataFrame shape: {combined_df.shape}")

    final_df = pd.merge(combined_df, parkzones_latlong_df, on="zone", how="left")

    print("Shapes after merging with Parkzones LatLong:")
    print(f"Final DataFrame shape: {final_df.shape}")

    final_df = final_df.rename(
        columns={"latitude": "latitude_zone", "longitude": "longitude_zone"}
    )

    return (
        final_df.astype(
            {
                "machine_ID": "Int64",
                "fee": "float64",
                "category": "object",
                "street": "object",
                "latitude_machine": "float64",
                "longitude_machine": "float64",
                "zone": "int64",
                "latitude_zone": "float64",
                "longitude_zone": "float64",
            }
        )
        .set_index("time")
        .sort_index()
    )


cale_df = process_excel_files("Cale")
parkster_df = process_excel_files("Parkster")

parkzones_latlong_df = load_parkzones_latlong(join(DATA_DIR, "parkzones_latlong.csv"))
parkzones_latlong_df.info()
parkzones_latlong_df.to_pickle("pickles/parkzones_latlong")

psa_latlong_df = load_psa_latlong(join(DATA_DIR, "psa_latlong.csv"))
psa_latlong_df.to_pickle("pickles/psa_latlong")

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
final_df.to_csv("out/final_df.csv")

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

print("\nComparison with Reference DataFrame:")
if final_df.shape == clean_df.shape and final_df.columns.equals(clean_df.columns):
    print("Shapes and columns match!")

    if final_df.equals(clean_df):
        print("Values match exactly!")
    else:
        print("Values differ.")
else:
    print("Shapes or columns do not match.")
