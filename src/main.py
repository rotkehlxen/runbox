import datetime as dt

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from auth import request_data
from models import GarminActivity
from style import (
    BINS,
    DARK_LAYOUT_SETTINGS,
    LIGHT_LAYOUT_SETTINGS,
    color_scale_labels,
    custom_color_scale,
    date_range,
    github_weekday,
    week_labels_x,
    week_of_year,
    weekday_labels_y,
)

TODAY = dt.date.today()
YEAR = TODAY.year


def main() -> None:
    # get data
    activities_raw = request_data(from_date=dt.date(YEAR, 1, 1), to_date=TODAY)
    # parse and validate data
    activities = [GarminActivity(**activity) for activity in activities_raw]
    # extract all running activities
    all_runs = [x for x in activities if x.activity_type.type_key == "running"]
    # export data to DataFrame
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


def create_plot_html(
    plot_data, hover_labels, year: int, num_colors: int, mode: str
) -> None:
    """
    Create the HTML for the plot.
    """
    layout_settings = DARK_LAYOUT_SETTINGS if mode == "dark" else LIGHT_LAYOUT_SETTINGS
    color_scale = custom_color_scale(num_colors=num_colors, mode=mode, hue=336)

    fig = go.Figure(
        go.Heatmap(
            z=plot_data.values,
            x=plot_data.columns,
            y=plot_data.index,
            zmax=num_colors - 1,
            zmin=0,
            colorscale=color_scale,
            xgap=2,
            ygap=2,
            colorbar=dict(
                title="km",
                **color_scale_labels(num_colors),
            ),
            hoverongaps=False,
            text=hover_labels.values,
            hovertemplate=(" %{text}<br>" + "<extra></extra>"),
        )
    )

    fig.update_xaxes(**week_labels_x(year))
    fig.update_yaxes(
        scaleanchor="x",
        autorange="reversed",
        tickmode="array",
        range=[-0.5, 6.5],
        **weekday_labels_y(),
    )

    fig.update_layout(width=1000, height=300, title="Running 2025", **layout_settings)

    fig.write_html("index.html")
