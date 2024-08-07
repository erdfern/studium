import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dsplotter import plot_map


def load_and_prepare_data(clean_df):
    machine_sales = clean_df[clean_df["category"] == "machine"]
    top_5_by_sales = (
        machine_sales.groupby("machine_ID")["fee"].sum().nlargest(5, "first")
    )

    weekly_sales = machine_sales[machine_sales["machine_ID"].isin(top_5_by_sales.index)]
    weekly_sales = (
        weekly_sales.groupby([pd.Grouper(freq="W"), "machine_ID"])["fee"]
        .sum()
        .reset_index()
    )

    return weekly_sales, top_5_by_sales


def plot_heatmap(weekly_sales):
    pivot_data = weekly_sales.pivot(index="time", columns="machine_ID", values="fee")

    # Add week numbers to the index
    pivot_data["week_number"] = pivot_data.index.isocalendar().week

    plt.figure(figsize=(20, 16))

    ax = sns.heatmap(
        pivot_data.iloc[:, :-1],
        cmap="YlOrRd",
        cbar_kws={"label": "Weekly Sales (EUR)"},
        annot=True,
        fmt=".2f",
        linewidths=0.5,
    )

    plt.xticks(rotation=0)

    # Set y-axis ticks to show every week number
    ax.set_yticks(range(len(pivot_data)))
    ax.set_yticklabels(pivot_data["week_number"], rotation=0)

    plt.title("Weekly Sales Heatmap for Top 5 Parking Machines (2023)")
    plt.xlabel("Machine ID")
    plt.ylabel("Week Number")
    plt.tight_layout()
    plt.savefig("out/top_5_machines_heatmap.png", dpi=300)
    plt.close()


def main():
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

    # 2.1.1
    weekly_sales, top_5_by_sales = load_and_prepare_data(clean_df)

    print(weekly_sales.head(5))

    # print("Top 5 machines by sales volume:")
    # print(top_5_by_sales)

    # plot_heatmap(weekly_sales)
    # /---
    # 2.1.2

    # yearly_sales_by_machine: pd.DataFrame = (
    #     clean_df[clean_df["category"] == "machine"]
    #     .groupby("machine_ID")[["fee", "latitude_machine", "longitude_machine"]]
    #     .agg(
    #         {
    #             "fee": "sum",
    #             "latitude_machine": "first",
    #             "longitude_machine": "first",
    #         }
    #     )
    # ).reset_index()  # reset_index() ensures that we get a DataFrame, which is only needed to silence the LSP (no functional difference)

    # yearly_sales_by_machine = yearly_sales_by_machine.rename(
    #     columns={
    #         "fee": "yearly_sales_eur",
    #         "latitude_machine": "latitude",
    #         "longitude_machine": "longitude",
    #     }
    # )

    # yearly_sales_by_machine.info()

    # print("\nYearly sales volume per machine:")
    # print(yearly_sales_by_machine)

    # plot_map(
    #     yearly_sales_by_machine, "yearly_sales_eur", "yearly_sales_eur", radius_scale=10
    # )

    # Observation regarding shared characteristics of machines with high sales volume:
    # Lesser distance to city center -> higher sales volume
    # Lesser distance to z-campus -> higher sales volume
    # ...?

    # 2.2
    sales_by_category_per_parkzone = (
        clean_df.groupby(["zone", "category"])["fee"]
        .agg(["sum", "count"])
        .reset_index()
        .rename(columns={"sum": "total_sales_volume", "count": "num_transactions"})
        .pivot_table(
            index=["zone", "category"],
            values=["total_sales_volume", "num_transactions"],
        )
    )

    print("\nSales by app and machine per parkzone:")
    print(sales_by_category_per_parkzone)
    sales_by_category_per_parkzone.info()

    df = sales_by_category_per_parkzone.reset_index()

    # Calculate totals per zone
    zone_totals = df.groupby("zone").sum()

    # Calculate percentages
    df["pct_transactions"] = df.apply(
        lambda row: row["num_transactions"]
        / zone_totals.loc[row["zone"], "num_transactions"]
        * 100,
        axis=1,
    )
    df["pct_sales_volume"] = df.apply(
        lambda row: row["total_sales_volume"]
        / zone_totals.loc[row["zone"], "total_sales_volume"]
        * 100,
        axis=1,
    )

    # Round percentages to 2 decimal places
    df["pct_transactions"] = df["pct_transactions"].round(2)
    df["pct_sales_volume"] = df["pct_sales_volume"].round(2)

    # Function to get the preferred category and its percentage
    def get_preferred_category(group):
        preferred = group.loc[group["pct_transactions"].idxmax()]
        return pd.Series(
            {
                "preferred_category": preferred["category"],
                "preferred_category_pct": preferred["pct_transactions"],
            }
        )

    # Function to get the highest grossing category and its percentage
    def get_highest_grossing_category(group):
        highest_grossing = group.loc[group["pct_sales_volume"].idxmax()]
        return pd.Series(
            {
                "highest_grossing_category": highest_grossing["category"],
                "highest_grossing_category_pct": highest_grossing["pct_sales_volume"],
            }
        )

    # Apply the functions to each zone
    result = (
        df.groupby("zone")
        .apply(get_preferred_category)
        .join(df.groupby("zone").apply(get_highest_grossing_category))
    )

    # Reset the index to make 'zone' a column again
    result = result.reset_index()

    # Create the final MultiIndex DataFrame
    final_df = df.set_index(["zone", "category"]).join(result.set_index("zone"))

    print(final_df)
    final_df.to_csv("final_df.csv")


if __name__ == "__main__":
    main()
