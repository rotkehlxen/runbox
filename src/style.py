import colorsys
import datetime as dt

import numpy as np
import pandas as pd


def hsl_to_hex(h, s, lightness):
    """Convert HSL (0-1) to HEX"""
    r, g, b = colorsys.hls_to_rgb(h, lightness, s)
    return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))


def custom_color_scale(num_colors: int, hue: int, saturation: float = 0.7) -> list:
    # green = 120
    hue = hue / 360

    # Choose [num_colorss] lightness values evenly spaced
    lightness_values = list(np.linspace(0.85, 0.15, num_colors))

    color_scale = [
        hsl_to_hex(hue, saturation, lightness) for lightness in lightness_values
    ]
    return ["#f0f0f0"] + color_scale  # including light gray as baseline color


def github_weekday(date: dt.date) -> int:
    """
    Github style for counting days in a week.
    Return 0 for Sunday, 1 for Monday etc.
    """
    return date.isoweekday() % 7


def week_of_year(date: dt.date, year: int) -> int:
    """
    In the isocalendar system, the last days in the year can be in the first week of the next year.
    To avoid this, we use this custom week of year function.
    """
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


def weekday_labels_y() -> list[str]:
    """
    Return labels for the days of the week in github style
    """
    return [
        "",
        "Mon  ",
        "",
        "Wed  ",
        "",
        "Fri  ",
        "",
    ]  # whitespaces for vertical alignment


def week_labels_x(year: int) -> list[str]:
    """
    Return labels for the weeks of the year in github style.
    Only the first week of each month is labeled with the corresponding month name.
    Returns [0, 5, 9, 13, ...], ["Jan", "Feb", "Mar", "Apr", ...]

    there must be an easier way to do this, but I don't know yet.
    """
    # date range for the year
    base = pd.DataFrame(
        {"date": date_range(dt.date(year, 1, 1), dt.date(year), 12, 31)}
    )
    base["month"] = base.date.apply(lambda x: x.strftime("%b"))
    base["calendar_week"] = base.date.apply(lambda x: week_of_year(x, 2025))
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
    return label_frame.calendar_week.to_list(), label_frame.month.to_list()
