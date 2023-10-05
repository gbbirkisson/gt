import csv
import json
import os
import subprocess
import sys
from datetime import datetime

import plotly.graph_objects as go
from plotly.subplots import make_subplots


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

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(
            x=timestamp,
            y=cpm,
            name="characters per minute",
            line=dict(color="firebrick", width=4),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=timestamp,
            y=wpm,
            name="words per minute",
            line=dict(color="orange", width=4),
        ),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(title_text=report_name)

    # Set x-axis title
    # fig.update_xaxes(title_text="time")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>words per minute</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>characters per minute</b>", secondary_y=True)

    # Add lines
    fig.add_hline(y=40, line_dash="dash", line_color="red", secondary_y=True)
    fig.add_hline(y=60, line_dash="dash", line_color="green", secondary_y=True)

    fig.show()


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
