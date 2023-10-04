import csv
import json
import os
import subprocess
import sys
from datetime import datetime

import matplotlib.dates as md
import matplotlib.pyplot as plt


def report_path(report_name: str) -> str:
    return f"{os.path.expanduser('~')}/.gt-{report_name}.csv"


def plot(report_name: str) -> None:
    timestamp = []
    wpm = []
    cpm = []

    with open(report_path(report_name), "r") as csvfile:
        lines = csv.reader(csvfile, delimiter=",")
        for row in [l for l in lines if l[0] == "test"]:
            timestamp.append(datetime.fromtimestamp(int(row[4])))
            wpm.append(int(row[1]))
            cpm.append(int(row[2]))

    assert len(wpm) > 0, f"No data in file {report_path(report_name)}"

    xfmt = md.DateFormatter("%Y-%m-%d")
    fig, ax1 = plt.subplots()
    ax1.xaxis.set_major_formatter(xfmt)

    color = "tab:red"
    ax1.set_xlabel("date")
    ax1.set_xticklabels(ax1.get_xticks(), rotation=10)
    ax1.set_ylabel("wpm", color=color)
    ax1.plot(timestamp, wpm, color=color)
    ax1.tick_params(axis="y", labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.xaxis.set_major_formatter(xfmt)

    color = "tab:blue"
    ax2.set_ylabel("cpm", color=color)  # we already handled the x-label with ax1
    ax2.plot(timestamp, cpm, color=color)
    ax2.tick_params(axis="y", labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()


def tt(items: list[dict[str, str]], report_name: str | None = None) -> None:
    try:
        process = subprocess.run(["tt", "-v"])
        assert process.returncode == 1
    except Exception:
        raise AssertionError(
            "Make sure tt is in your path: https://github.com/lemnos/tt/releases"
        )

    input = json.dumps(items).encode("utf-8")
    args = ["tt", "-quotes", "-", "-noskip", "-noreport"]

    if report_name:
        args.extend(["-csv"])
        with open(report_path(report_name), "a") as report:
            process = subprocess.run(
                args,
                check=False,
                shell=False,
                input=input,
                stdout=report,
            )
    else:
        process = subprocess.run(args, check=False, shell=False, input=input)

    sys.exit(process.returncode)
