import datetime as dt
import json

import pandas as pd

from models import GarminActivity
from style import date_range


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

    pass


def process_data(
    data: pd.DataFrame, year: int, bins=[-1, 0, 3, 5, 8, 100], hue: int = 336
) -> pd.DataFrame:
    """
    Process the data for visualization.
    This is done for a particular [year] (running data from one year are shown).
    The color scale is descrete and has len(bins) - 1 colors. Bins indicate km ranges.
    The first bin is for 0 km (gray color), the last bin is for > 8 km.
    [hue] is the hur of the color scale in degrees (0-360).
    """
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
