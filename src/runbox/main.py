import datetime as dt

import pandas as pd

from runbox.auth import request_data
from runbox.models import GarminActivity
from runbox.plot import create_plot_html, process_data
from runbox.style import (
    BINS,
)

NOW = dt.datetime.now()
TODAY = NOW.date()
YEAR = TODAY.year
TITLE = f"Running {YEAR} (last updated on {NOW.strftime('%-d.%-m.%Y at %-I:%M%p')})"


def update_chart() -> None:
    # get data
    run_activities_raw = request_data(from_date=dt.date(YEAR, 1, 1), to_date=TODAY)
    # parse and validate data
    all_runs = [GarminActivity(**activity) for activity in run_activities_raw]
    # export seleted data fields to DataFrame
    data = pd.DataFrame([GarminActivity.export(run) for run in all_runs])
    # process data for visualization
    plot_data, hover_labels = process_data(data=data, year=YEAR, bins=BINS)
    # plot and create HTML
    create_plot_html(
        plot_data=plot_data,
        hover_labels=hover_labels,
        year=YEAR,
        num_colors=len(BINS),
        mode="light",
        title=TITLE,
    )
    print("Successfully created the plot in index.html.")


if __name__ == "__main__":
    update_chart()
