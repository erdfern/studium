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


# 2.2.2
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
        pd.read_pickle("pickles/clean_df")
        if os.path.exists("pickles/clean_df")
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

    df221 = zone_agg.join(transactions_by_category).join(sales_volume_by_category)

    df221 = df221.reset_index()

    df221["app_usage_rate"] = df221["transactions_app"] / df221["total_transactions"]
    df221["machine_usage_rate"] = (
        df221["transactions_machine"] / df221["total_transactions"]
    )

    df221.info()

    # df_melted221 = df221.melt(
    #     id_vars=["zone"],
    #     value_vars=["app_usage_rate", "machine_usage_rate"],
    #     var_name="variable",
    #     value_name="value",
    # )

    # plt.figure(figsize=(12, 6))
    # sns.barplot(x="zone", y="value", hue="variable", data=df_melted221)

    # plt.xlabel("Park Zone")
    # plt.ylabel("Usage Rate")
    # plt.title("App vs. Machine Usage Rate per Park Zone in 2023")
    # plt.xticks(rotation=45)
    # plt.legend(title="Usage Type")

    # plt.gca().yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    # plt.ylim(0.0, 1.0)

    # plt.savefig("out/2.2.1.png")

    # 2.2.2
    # df_melted221 = df221.melt(
    #     id_vars=["zone"],
    #     value_vars=["total_transactions", "transactions_machine"],
    #     var_name="variable",
    #     value_name="value",
    # )

    # plt.figure(figsize=(10, 6))
    # ax = sns.barplot(x="zone", y="value", hue="variable", data=df_melted221)
    # handles, labels = ax.get_legend_handles_labels()
    # custom_labels = ["Total Transactions", "Machine Transactions"]
    # ax.legend(handles, custom_labels)

    # plt.yscale("log")

    # plt.title("Total Transactions vs Machine Transactions per Zone (Log Scale)")
    # plt.xlabel("Zone")
    # plt.ylabel("Transactions")

    # plt.xticks(rotation=45)

    # plt.savefig("out/2.2.2.png")

    # 2.2.3
    psa_latlong_df = pd.read_pickle("pickles/psa_latlong")

    # machines_per_zone = (
    #     psa_latlong_df.groupby("zone").size().to_frame(name="machines_per_zone")
    # )

    # df223 = df221.merge(machines_per_zone, on="zone")
    # df221.info()
    # print(df221.head(5))

    # df223["normalized_transactions"] = (
    #     df223["total_transactions"] / df223["machines_per_zone"]
    # )
    # df223["normalized_machine_transactions"] = (
    #     df223["transactions_machine"] / df223["machines_per_zone"]
    # )

    # busiest_zone = df223.loc[df223["normalized_transactions"].idxmax(), "zone"]
    # print(f"The busiest parkzone is: {busiest_zone}")

    # Melt the dataframe to have `normalized_transactions` and `normalized_machine_transactions` in one column
    # df_melted223 = df223.melt(
    #     id_vars=["zone"],
    #     value_vars=["normalized_transactions", "normalized_machine_transactions"],
    #     var_name="variable",
    #     value_name="value",
    # )

    # plt.figure(figsize=(10, 6))
    # ax = sns.barplot(x="zone", y="value", hue="variable", data=df_melted223)
    # handles, labels = ax.get_legend_handles_labels()
    # custom_labels = ["Total Transactions", "Machine Transactions"]
    # ax.legend(handles, custom_labels)

    # plt.yscale("log")
    # plt.title(
    #     "Normalized Transactions vs Normalized Machine Transactions per Zone (Log Scale)"
    # )
    # plt.xlabel("Zone")
    # plt.ylabel("Normalized Transactions")
    # plt.xticks(rotation=45)

    # plt.text(
    #     0.0,
    #     1.0,
    #     f"Busiest Zone (total): {busiest_zone}",
    #     transform=plt.gca().transAxes,
    #     ha="left",
    #     va="top",
    # )

    # plt.savefig("out/2.2.3.png")

    # 2.2.4
    parkzones_latlong = pd.read_pickle("pickles/parkzones_latlong")
    parkzones_latlong.info()
    df224 = df221.merge(parkzones_latlong, on="zone")
    # plot_map(df224, "machine_usage_rate", "transactions_machine", radius_scale=10)

    # 3.1 - t-test
    # 1. Determine daily rate of machine use per parkzone
    daily_sales_parkzone = sales_df.groupby([pd.Grouper(freq="D"), "zone"])
    daily_sales_parkzone_app = sales_df[sales_df["category"] == "app"].groupby(
        [pd.Grouper(freq="D"), "zone"]
    )
    daily_sales_parkzone_machine = sales_df[sales_df["category"] == "machine"].groupby(
        [pd.Grouper(freq="D"), "zone"]
    )
    sales_counts = daily_sales_parkzone["fee"].count().to_frame(name="sales_total")

    # sales_counts["sales_app"] = daily_sales_parkzone_app["fee"].count()
    sales_counts["sales_machine"] = daily_sales_parkzone_machine["fee"].count()
    sales_counts = sales_counts.astype(
        {"sales_total": "int64", "sales_machine": "Int64"}
    )

    sales_counts["rate_machine"] = (
        sales_counts["sales_machine"] / sales_counts["sales_total"]
    )
    sales_counts["rate_machine"] = sales_counts["rate_machine"].fillna(0.0)

    average_machine_usage_per_zone = sales_counts.groupby(["zone"])[
        "rate_machine"
    ].mean()
    print(average_machine_usage_per_zone.to_markdown())

    # 2. For each parkzone, carry out a t-test which tests wheter parkers prefer to use the app in the respective zone

    # Hypotheses for the t-test
    #     Null Hypothesis (H0): The proportion of app usage in a given zone is equal to or greater than the proportion of machine usage. (In other words, parkers do not prefer the app in that zone)
    #     Alternative Hypothesis (HA): The proportion of app usage in a given zone is less than the proportion of machine usage. (Parkers prefer to use the machine in that zone)
    # Since we're dealing with proportions and comparing them to a theoretical value (0.5, implying no preference), we'll use a one-sample t-test.
    from scipy import stats

    # sales_counts.info()

    for zone, rate_machine in average_machine_usage_per_zone.items():
        rate_app = 1 - rate_machine

        # Filter sales_counts by zone using .xs()
        zone_data = sales_counts.xs(zone, level="zone")
        # print(zone_data)

        t_statistic, p_value = stats.ttest_1samp(zone_data["rate_machine"], 0.5, alternative="greater")

        if p_value < 0.05:
            print(
                f"Zone {zone}: Reject H0. Parkers prefer to use the machine. (p-value = {p_value:.4f})"
            )
        else:
            print(
                f"Zone {zone}: Fail to reject H0. No evidence of preference for the machine. (p-value = {p_value:.4f})"
            )


if __name__ == "__main__":
    main()
