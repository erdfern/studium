import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dsplotter import plot_map


def load_and_prepare_data(clean_df):
    machine_sales = clean_df[clean_df["category"] == "machine"]
    top_5_by_sales = (
        machine_sales.groupby("machine_ID")["fee"].sum().nlargest(5, "first")
    )

    weekly_sales = machine_sales[
        machine_sales["machine_ID"].isin(top_5_by_sales.index)
    ]
    weekly_sales = (
        weekly_sales.groupby([pd.Grouper(freq="W"), "machine_ID"])["fee"]
        .sum()
        .reset_index()
    )

    return weekly_sales, top_5_by_sales


def plot_heatmap(weekly_sales):
    pivot_data = weekly_sales.pivot(
        index="time", columns="machine_ID", values="fee"
    )

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

    print("Top 5 machines by sales volume:")
    print(top_5_by_sales)

    plot_heatmap(weekly_sales)
    # /---
    # 2.1.2

    yearly_sales_by_machine: pd.DataFrame = (
        clean_df[clean_df["category"] == "machine"]
        .groupby("machine_ID")[
            ["fee", "latitude_machine", "longitude_machine"]
        ]
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

    print("\nYearly sales per machine and location:")
    print(yearly_sales_by_machine)

    plot_map(yearly_sales_by_machine, "yearly_sales_eur", "yearly_sales_eur", radius_scale=10)

    # Observation regarding shared characteristics of machines with high sales volume:
    # Lesser distance to city center -> higher sales volume
    # Lesser distance to z-campus -> higher sales volume
    # ...?


if __name__ == "__main__":
    main()
