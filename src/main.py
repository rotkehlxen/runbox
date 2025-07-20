import datetime as dt
import json

import numpy as np
import pandas as pd

from models import GarminActivity
from style import date_range, github_weekday, week_of_year


def main() -> None:
    # get data (will be an API call later)
    with open("garmin_data.json", "r") as f:
        activities = json.load(f)
    # parse and validate data
    all_activities = [GarminActivity(**activity) for activity in activities]
    # extract all running activities
    all_runs = [x for x in all_activities if x.activity_type.type_key == "running"]
    # export data to DataFrame
    data = pd.DataFrame([GarminActivity.export(run) for run in all_runs])
    # process data for visualization
    plot_data, hover_labels = process_data(
        data=data, year=2025, bins=[-1, 0, 3, 5, 8, 100]
    )
    pass


def process_data(
    data: pd.DataFrame, year: int, bins: list[int]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Process the data for visualization.
    This is done for a particular [year] (running data from one year are shown).
    Bins indicate km ranges.
    """
    num_colors = len(bins) - 1
    # aggregate running distances and durations by date
    data = (
        data.groupby("date")
        .agg({"distance_km": "sum", "duration_min": "sum", "place": "first"})
        .reset_index()
        .copy()
    )
    # filter for data in [year] and fill in missing dates (with 0 distance and duration)
    base = pd.DataFrame(
        {"date": date_range(dt.date(year, 1, 1), dt.date(year, 12, 31))}
    )
    data = pd.merge(base, data, on="date", how="left").fillna(0)

    # add columns for plotting
    data["github_weekday"] = data.date.apply(lambda x: github_weekday(x))
    data["calendar_week"] = data.date.apply(lambda x: week_of_year(x, 2025))
    data["distance_bin"] = pd.cut(
        data.distance_km.round(), bins=bins, labels=list(range(num_colors))
    )
    data["hover_label"] = data.apply(
        lambda row: f"{np.round(row['distance_km'], 3)} km <br> {row['date']}\
                                     {'in ' + row['place'] if row['place'] != 0 else ''}",
        axis=1,
    )
    # return plot data and hover labels
    return data.pivot(
        index="github_weekday", columns="calendar_week", values="distance_bin"
    ), data.pivot(index="github_weekday", columns="calendar_week", values="hover_label")
