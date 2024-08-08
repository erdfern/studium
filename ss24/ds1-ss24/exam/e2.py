import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from dsplotter import plot_map


def _load_and_prepare_data(clean_df):
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


def _plot_heatmap(weekly_sales):
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
    plt.savefig("out/top_5_machines_heatmap.png", dpi=300)
    plt.close()


def analyze_machine_sales(sales_df: pd.DataFrame):
    weekly_sales, top_5_by_sales = _load_and_prepare_data(sales_df)

    print(weekly_sales.head(5))

    print("Top 5 machines by sales volume:")
    print(top_5_by_sales)

    _plot_heatmap(weekly_sales)

    yearly_sales_by_machine: pd.DataFrame = (
        sales_df[sales_df["category"] == "machine"]
        .groupby("machine_ID")[["fee", "latitude_machine", "longitude_machine"]]
        .agg(
            {
                "fee": "sum",
                "latitude_machine": "first",
                "longitude_machine": "first",
            }
        )
    ).reset_index()  # reset_index() ensures that we get a DataFrame, which is only needed to silence the LSP (no functional difference)

    yearly_sales_by_machine = yearly_sales_by_machine.rename(
        columns={
            "fee": "yearly_sales_eur",
            "latitude_machine": "latitude",
            "longitude_machine": "longitude",
        }
    )

    yearly_sales_by_machine.info()

    print("\nYearly sales volume per machine:")
    print(yearly_sales_by_machine)

    plot_map(
        yearly_sales_by_machine, "yearly_sales_eur", "yearly_sales_eur", radius_scale=10
    )

    # Observation regarding shared characteristics of machines with high sales volume:
    # Lesser distance to city center -> higher sales volume
    # Lesser distance to z-campus -> higher sales volume
    # ...?


def main():
    sales_df = (
        pd.read_pickle("pickles/clean_df.pickle")
        if os.path.exists("pickles/clean_df.pickle")
        else pd.read_csv(
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
    )

    # 2.1

    # analyze_machine_sales(sales_df)

    # 2.2
    # Group by `zone` and count the number of rows to get `total_transactions`
    zone_agg = sales_df.groupby("zone").size().to_frame(name="total_transactions")

    # Group by `zone` and sum the `fee` column to get `total_sales_volume`
    zone_agg["total_sales_volume"] = sales_df.groupby("zone")["fee"].sum()

    # Group by `zone` and `category`, then count the number of rows
    transactions_by_category = sales_df.groupby(["zone", "category"]).size()

    # Pivot the result to have `category` as columns and fill missing values with 0
    transactions_by_category = transactions_by_category.unstack(fill_value=0)

    transactions_by_category = transactions_by_category.rename(
        columns={"app": "transactions_app", "machine": "transactions_machine"}
    )

    sales_volume_by_category = sales_df.groupby(["zone", "category"])["fee"].sum()

    sales_volume_by_category = sales_volume_by_category.unstack(fill_value=0)
    sales_volume_by_category = sales_volume_by_category.rename(
        columns={"app": "sales_volume_app", "machine": "sales_volume_machine"}
    )

    df = zone_agg.join(transactions_by_category).join(sales_volume_by_category)

    df = df.reset_index()

    print(df.to_markdown())
    df.info()
    # df.to_csv("df.csv")

    df["app_usage_rate"] = df["transactions_app"] / df["total_transactions"]
    df["machine_usage_rate"] = df["transactions_machine"] / df["total_transactions"]

    df_melted = df.melt(
        id_vars=["zone"],
        value_vars=["app_usage_rate", "machine_usage_rate"],
        var_name="variable",
        value_name="value",
    )

    plt.figure(figsize=(12, 6))
    sns.barplot(x="zone", y="value", hue="variable", data=df_melted)

    plt.xlabel("Park Zone")
    plt.ylabel("Usage Rate")
    plt.title("App vs. Machine Usage Rate per Park Zone in 2023")
    plt.legend(title="Usage Type")

    plt.gca().yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    plt.ylim(0.0, 1.0)

    plt.savefig("out/2.2.1.png")

    # 2.2.2
    df_melted = df.melt(id_vars=["zone"], value_vars=["total_transactions", "transactions_machine"], var_name="variable", value_name="value")

    plt.figure(figsize=(10, 6))
    sns.barplot(x="zone", y="value", hue="variable", data=df_melted)

    plt.yscale('log')

    plt.title('Total Transactions vs Machine Transactions per Zone (Log Scale)')
    plt.xlabel('Zone')
    plt.ylabel('Transactions')

    plt.savefig("out/2.2.2.png")

if __name__ == "__main__":
    main()
