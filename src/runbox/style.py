import colorsys
import datetime as dt

import numpy as np
import pandas as pd

MUDDY_WHITE = "#C9D1D9"
DARK_LAYOUT_SETTINGS = {
    "plot_bgcolor": "black",
    "paper_bgcolor": "black",
    "font": {"color": MUDDY_WHITE},
    "xaxis": dict(color=MUDDY_WHITE, gridcolor="black", zeroline=False),
    "yaxis": dict(color=MUDDY_WHITE, gridcolor="black", zeroline=False),
}
LIGHT_LAYOUT_SETTINGS = {"plot_bgcolor": "white"}

BINS = [-1, 0, 3, 5, 8, 100]


def hsl_to_hex(hue, saturation, lightness) -> str:
    """
    Convert HSL (0-1) to HEX
    Uusally hue is in [0, 360] range, but here we use [0, 1] for consistency with other functions.
    """

    r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
    return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))


def custom_color_scale(
    num_colors: int, mode: str, hue: int, saturation: float = 0.7
) -> list:
    """
    Create a custom color scale for the heatmap with one color indicating no acitivity
    (light gray in light mode, dark gray in dark mode). Color scale is created with
    [hue] and [saturation] parameters in [num_colors] lightness values.
    [hue] is in range [0, 360]
    """
    # green = 120
    hue = hue / 360

    # empty color
    empty_col = "#333333" if mode == "dark" else "#f0f0f0"

    # Choose [num_colorss] lightness values evenly spaced
    lightness_values = list(np.linspace(0.85, 0.15, num_colors - 1))

    color_scale = [
        hsl_to_hex(hue, saturation, lightness) for lightness in lightness_values
    ]
    return [empty_col] + color_scale  # including light gray as baseline color


def github_weekday(date: dt.date) -> int:
    """
    Github style for counting days in a week.
    Return 0 for Sunday, 1 for Monday etc.
    """
    return date.isoweekday() % 7


def week_of_year(date: dt.date) -> int:
    """
    Return the week of the year for a given [date] in the [year].
    In the isocalendar system, the last days in the year can be in the first week of the next year.
    To avoid this, we use this custom week of year function.
    """
    year = date.year
    # tm_yday provides the number of the day in the year
    return (date.timetuple().tm_yday + github_weekday(dt.date(year, 1, 1)) - 1) // 7


def date_range(date_from: dt.date, date_to: dt.date) -> list[dt.date]:
    """
    Create list of dates from [date_from] to [date_to] including the
    from and to dates.
    """
    return [
        date_from + dt.timedelta(days=i) for i in range((date_to - date_from).days + 1)
    ]


def weekday_labels_y() -> dict:
    """
    Return labels for the days of the week in github style
    """
    return {
        "tickvals": list(range(7)),
        "ticktext": [
            "",
            "Mon  ",
            "",
            "Wed  ",
            "",
            "Fri  ",
            "",
        ],
    }  # whitespaces for vertical alignment


def week_labels_x(year: int) -> dict:
    """
    Return labels for the weeks of the year (x axis) in github style.
    Only the first week of each month is labeled with the corresponding month name.
    Returns [0, 5, 9, 13, ...], ["Jan", "Feb", "Mar", "Apr", ...]

    there must be an easier way to do this, but I don't know yet.
    """
    # date range for the year
    base = pd.DataFrame(
        {"date": date_range(dt.date(year, 1, 1), dt.date(year, 12, 31))}
    )
    base["month"] = base.date.apply(lambda x: x.strftime("%b"))
    base["calendar_week"] = base.date.apply(lambda x: week_of_year(x))
    # count the days in every month_week
    days_per_month_week = (
        base.groupby(["calendar_week", "month"])
        .size()
        .reset_index(name="count_days")
        .sort_values(["calendar_week", "count_days"])
    )
    # every calendar week gets assigned only one month (the one that covers more days of that week)
    dedup = days_per_month_week.drop_duplicates(subset=["calendar_week"], keep="last")[
        ["calendar_week", "month"]
    ]
    # only one calendarweek per month (the first one in the month)
    label_frame = dedup.drop_duplicates(subset=["month"], keep="first")
    # return tickvals, ticktext
    return {
        "tickvals": label_frame.calendar_week.to_list(),
        "ticktext": label_frame.month.to_list(),
    }


def color_scale_labels(num_colors: int) -> dict:
    # return tickvals, ticktext
    lc = [""] * (num_colors)
    lc[0] = "less"
    lc[-1] = "more"
    return {"tickvals": list(range(num_colors)), "ticktext": lc}
