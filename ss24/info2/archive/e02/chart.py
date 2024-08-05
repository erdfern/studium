import matplotlib.pyplot as plt
import pandas as pd


# processes = ["P1", "P2", "P3", "P4", "P5", "P6"]
# arrival_times = [0, 15000, 35000, 40000, 90000, 115000]
# burst_times = [15000, 20000, 5000, 50000, 25000, 10000]


def fcfs_scheduling(processes):
    n = len(processes)

    completed_processes = []
    states = []

    time = min(a["arrival_time"] for a in processes.values())

    while len(completed_processes) < n:
        # run the process with the earliest arrival time
        process_id, arrival_time = min(
            (p, a["arrival_time"])
            for p, a in processes.items()
            if not any(p == cp["id"] for cp in completed_processes)
        )

        burst_time = processes[process_id]["burst_time"]
        start_time = time
        end_time = start_time + burst_time
        wait_time = start_time - arrival_time

        arrived_during_run = [
            p
            for p, a in processes.items()
            if (
                p != process_id
                and not any(p == cp["id"] for cp in completed_processes)
                and a["arrival_time"] in range(start_time, end_time)
            )
        ]

        states.append(
            {
                "t": time,
                "P": process_id,
                "W": arrived_during_run,
                'P_"complete"': [cp["id"] for cp in completed_processes],
            }
        )

        completed_processes.append(
            {
                "id": process_id,
                't_"arrival"': arrival_time,
                't_"start"': start_time,
                't_"end"': end_time,
                "w": wait_time,
            }
        )

        time = end_time

    # end state
    states.append(
        {
            "t": time,
            "P": None,
            "W": [],
            'P_"complete"': [p["id"] for p in completed_processes],
        }
    )

    completed_processes = pd.DataFrame(completed_processes)
    states = pd.DataFrame(states)
    completed_processes.set_index("id", inplace=True)
    states.set_index("t", inplace=True)
    return states, completed_processes


def round_robin_scheduling(processes, time_quantum):
    time = 0
    wait_queue = []
    completed_processes = []
    states = []

    def next_process():
        return wait_queue.pop(0) if wait_queue else None

    def add_to_wait_queue(process_id, burst_time, arrival_time, activity_intervals):
        wait_queue.append((process_id, burst_time, arrival_time, activity_intervals))

    def process_completed(
        process_id, arrival_time, start_time, end_time, activity_intervals
    ):
        total_wait_time = activity_intervals[0][0] - arrival_time
        total_wait_time += sum(
            activity_intervals[i][0] - activity_intervals[i - 1][1]
            for i in range(1, len(activity_intervals))
        )

        completed_processes.append(
            {
                "id": process_id,
                't_"arrival"': arrival_time,
                't_"start"': start_time,
                't_"end"': end_time,
                "w": total_wait_time,
                "A": activity_intervals,
            }
        )

    while len(completed_processes) < len(processes) or wait_queue:
        if not wait_queue:
            process_id, arrival_time = min(
                (p, a["arrival_time"])
                for p, a in processes.items()
                if not any(p == cp["id"] for cp in completed_processes)
            )
            burst_time = processes[process_id]["burst_time"]
            start_time = arrival_time
            time = arrival_time
            activity_intervals = []
        else:
            process_id, burst_time, arrival_time, activity_intervals = next_process()
            start_time = time

        run_time = min(time_quantum, burst_time)
        time += run_time
        burst_time -= run_time
        active_interval = (start_time, time)

        activity_intervals.append(active_interval)

        states.append(
            {
                "t": start_time,
                "P": process_id,
                # put only the IDs of the processes in the wait_queue and their remaining burst_time
                "W": [(p, b) for p, b, _, _ in wait_queue],
                'P_"complete"': [p["id"] for p in completed_processes],
            }
        )

        # check if there are arrivals during the run
        # don't add self to wait_queue, don't add if already in wait_queue
        for p, a in processes.items():
            if (
                p != process_id
                and a["arrival_time"] in range(start_time, time)
                and not any(p == wq[0] for wq in wait_queue)
            ):
                add_to_wait_queue(p, a["burst_time"], a["arrival_time"], [])

        # TODO: Sünde. Clean up.
        # check if process is completed
        if burst_time == 0:
            process_completed(
                process_id, arrival_time, start_time, time, activity_intervals
            )
        elif len(wait_queue) == 0:
            end_time = time + burst_time
            no_new_arrivals = all(
                a["arrival_time"] <= end_time
                for p, a in processes.items()
                if p != process_id
            )
            if no_new_arrivals:
                active_interval = (start_time, end_time)
                activity_intervals.pop()
                activity_intervals.append(active_interval)

                process_completed(
                    process_id, arrival_time, start_time, end_time, activity_intervals
                )

                states.append(
                    {
                        "t": end_time,
                        "P": None,
                        # only the IDs of the processes in the wait_queue and their remaining burst_time
                        "W": [(p, b) for p, b, _, _ in wait_queue],
                        'P_"complete"': [p["id"] for p in completed_processes],
                    }
                )
            else:
                add_to_wait_queue(
                    process_id, burst_time, arrival_time, activity_intervals
                )

        else:
            add_to_wait_queue(process_id, burst_time, arrival_time, activity_intervals)

    states_df = pd.DataFrame(states)
    states_df.set_index("t", inplace=True)
    completed_df = pd.DataFrame(completed_processes)
    completed_df.set_index("id", inplace=True)
    return (states_df, completed_df)


def get_completion_times(completion_times):
    return {process_id: time for process_id, time in completion_times.items()}


def print_markdown_table(df):
    print(df.to_markdown())


def write_markdown_table(df, filename):
    df.to_markdown(buf=filename, index=False)


def test_round_robin_sim():
    test_cases = [
        {
            "name": "control",
            "processes": {
                "P1": {"arrival_time": 0, "burst_time": 6},
                "P2": {"arrival_time": 2, "burst_time": 6},
                "P3": {"arrival_time": 4, "burst_time": 5},
                "P4": {"arrival_time": 12, "burst_time": 4},
                "P5": {"arrival_time": 16, "burst_time": 3},
                "P6": {"arrival_time": 19, "burst_time": 6},
            },
            "time_quantum": 5,
            "expected_completion_times": {
                "P1": 16,
                "P2": 17,
                "P3": 15,
                "P4": 21,
                "P5": 24,
                "P6": 30,
            },
        }
    ]

    for test_case in test_cases:
        print(f"Running {test_case['name']}...")
        states, completed = round_robin_scheduling(
            test_case["processes"], test_case["time_quantum"]
        )

        # for every process in the test case, check that the process completed at the expected time
        # get the process IDs and completion times from the completed processes
        completion_times = get_completion_times(completed['t_"end"'])

        # check that the completion times match the expected completion times
        for key, value in completion_times.items():
            assert (
                value == test_case["expected_completion_times"][key]
            ), f"{test_case['name']} failed: Expected {test_case['expected_completion_times'][key]} but got {value}"

        print(f"{test_case['name']} passed")


def plot_gantt_chart_fcfs(df):
    df.sort_index(inplace=True, ascending=False)
    fig, ax = plt.subplots(figsize=(16, 8))

    # Plot the waiting times
    for idx, (i, row) in enumerate(df.iterrows()):
        ax.broken_barh(
            [(row['t_"arrival"'], row["w"])],
            (idx - 0.4, 0.8),
            facecolors="gray",
            edgecolor="black",
            hatch="///",
            alpha=0.5,
            linestyle="dashed",
        )

    # Plot the running times
    for idx, (i, row) in enumerate(df.iterrows()):
        ax.broken_barh(
            [(row['t_"start"'], row['t_"end"'] - row['t_"start"'])],
            (idx - 0.4, 0.8),
            # facecolors="blue",
            facecolors="C0",
            edgecolor="black",
        )

    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(df.index)
    ax.set_xlabel("t")
    ax.set_ylabel("Prozess")
    ax.set_title("FCFS Lauf- und Wartezeiten")

    # plt.show()
    plt.savefig("build/fcfs_gantt.png")


def calculate_waiting_intervals(row):
    print("row", row)
    intervals = []
    prev_end = row['t_"arrival"']

    for start, end in row["A"]:
        if start > prev_end:
            intervals.append((prev_end, start))
            prev_end = end
        else:
            prev_end = end

    return intervals


def plot_gantt_chart_rr(df):
    df["waiting_intervals"] = df.apply(calculate_waiting_intervals, axis=1)
    df = df.sort_index(ascending=False)

    fig, ax = plt.subplots(figsize=(16, 8))

    # Define a color map for processes
    colors = {
        "P_1": "C0",
        "P_2": "C1",
        "P_3": "C2",
        "P_4": "C3",
        "P_5": "C4",
        "P_6": "C5",
    }

    for p, a in df.iterrows():
        process_color = colors[p]
        for duration in a["A"]:
            ax.barh(
                p,
                left=duration[0],
                width=duration[1] - duration[0],
                color=process_color,
            )

        for waiting_interval in a["waiting_intervals"]:
            ax.barh(
                p,
                left=waiting_interval[0],
                width=waiting_interval[1] - waiting_interval[0],
                color="gray",
                linestyle="dashed",
                hatch="///",
                alpha=0.5,
            )

    ax.set_xlabel("t")
    ax.set_ylabel("Prozess")
    ax.set_title("Round Robin Lauf- und Wartezeiten")

    plt.savefig("build/rr_gantt.png")
    # plt.show()


if __name__ == "__main__":
    test_round_robin_sim()

    processes = {
        "P_1": {"arrival_time": 0, "burst_time": 15000},
        "P_2": {"arrival_time": 4000, "burst_time": 20000},
        "P_3": {"arrival_time": 5000, "burst_time": 5000},
        "P_4": {"arrival_time": 39000, "burst_time": 50000},
        "P_5": {"arrival_time": 42000, "burst_time": 25000},
        "P_6": {"arrival_time": 43000, "burst_time": 10000},
    }
    time_quantum = 5000

    # processes = {
    #     "P_1": {"arrival_time": 0, "burst_time": 6},
    #     "P_2": {"arrival_time": 2, "burst_time": 6},
    #     "P_3": {"arrival_time": 4, "burst_time": 5},
    #     "P_4": {"arrival_time": 12, "burst_time": 4},
    #     "P_5": {"arrival_time": 16, "burst_time": 3},
    #     "P_6": {"arrival_time": 19, "burst_time": 6},
    # }
    # time_quantum = 5

    fcfs_states, fcfs_completed = fcfs_scheduling(processes)
    plot_gantt_chart_fcfs(fcfs_completed)
    fcfs_states.columns = [f"${c}$" for c in fcfs_states.columns]
    fcfs_completed.columns = [f"${c}$" for c in fcfs_completed.columns]
    print("First Come First Serve Scheduling")
    # print_markdown_table(fcfs_states)
    print_markdown_table(fcfs_completed)
    print(f"Mean waiting time: {fcfs_completed['$w$'].mean()}")
    fcfs_states.to_markdown(buf="build/fcfs_steps.md")
    fcfs_completed.to_markdown(buf="build/fcfs_result.md")

    rr_states, rr_completed = round_robin_scheduling(processes, time_quantum)
    # print(rr_completed.describe())
    plot_gantt_chart_rr(rr_completed)
    rr_states.columns = [f"${c}$" for c in rr_states.columns]
    rr_completed.columns = [f"${c}$" for c in rr_completed.columns]
    print("Round Robin Scheduling")
    # print_markdown_table(rr_states)
    print_markdown_table(rr_completed)
    print(f"Mean waiting time: {rr_completed['$w$'].mean()}")
    rr_states.to_markdown(buf="build/round_robin_steps.md")
    rr_completed.to_markdown(buf="build/round_robin_result.md")
