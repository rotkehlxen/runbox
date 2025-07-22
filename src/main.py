import datetime as dt

import pandas as pd

from auth import request_data
from models import GarminActivity
from plot import create_plot_html, process_data
from style import (
    BINS,
)

TODAY = dt.date.today()
YEAR = TODAY.year


def main() -> None:
    # get data
    run_activities_raw = request_data(from_date=dt.date(YEAR, 1, 1), to_date=TODAY)
    # parse and validate data
    all_runs = [GarminActivity(**activity) for activity in run_activities_raw]
    # export seleted data to DataFrame
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
    )
    print("Successfully created the plot in index.html.")


if __name__ == "__main__":
    main()
