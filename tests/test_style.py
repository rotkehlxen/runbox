import datetime as dt

from runbox.style import (
    custom_color_scale,
    date_range,
    github_weekday,
    hsl_to_hex,
    week_of_year,
)


def test_github_weekday():
    # 27th of July 2025 is a Sunday - should return day 0
    assert github_weekday(dt.date(2025, 7, 27)) == 0
    # 28th of July 2025 is a Monday - should return day 1
    assert github_weekday(dt.date(2025, 7, 28)) == 1
    # 29th of July 2025 is a Tuesday - should return day 2
    assert github_weekday(dt.date(2025, 7, 29)) == 2
    # 30th of July 2025 is a Wednesday - should return day 3
    assert github_weekday(dt.date(2025, 7, 30)) == 3
    # 31st of July 2025 is a Thursday - should return day 4
    assert github_weekday(dt.date(2025, 7, 31)) == 4
    # 1st of August 2025 is a Friday - should return day 5
    assert github_weekday(dt.date(2025, 8, 1)) == 5
    # 2nd of August 2025 is a Saturday - should return day 6
    assert github_weekday(dt.date(2025, 8, 2)) == 6


def test_week_of_year():
    # 1st of January 2025 should be in week 0
    assert week_of_year(dt.date(2025, 1, 1)) == 0
    # 31st of Dec should be in week 52 (and not week 1 of the next year as usual)
    assert week_of_year(dt.date(2025, 12, 31)) == 52
    # a new week starts on a Sunday, so 4th of Jan 2026 should be in week 1
    assert week_of_year(dt.date(2026, 1, 4)) == 1


def test_date_range():
    # create a date range from 1st to 3rd of January 2025
    dates = date_range(dt.date(2025, 1, 1), dt.date(2025, 1, 3))
    assert len(dates) == 3
    assert dates[0] == dt.date(2025, 1, 1)
    assert dates[1] == dt.date(2025, 1, 2)
    assert dates[2] == dt.date(2025, 1, 3)


def test_custom_color_scale():
    # light mode -----
    colors = custom_color_scale(num_colors=5, mode="light", hue=120)
    assert len(colors) == 5
    # Check if all colors are strings
    assert all(isinstance(color, str) for color in colors)
    # Check that all colors start with '#' (are hexadecimal)
    assert all(color.startswith("#") for color in colors)
    # Check the id of the first color (empty color)
    assert colors[0] == "#f0f0f0"  # light gray for light mode
    # check that all colors are different
    assert len(set(colors)) == len(colors)

    # dark mode -----
    dark_colors = custom_color_scale(num_colors=5, mode="dark", hue=120)
    assert dark_colors[0] == "#333333"  # dark gray for dark mode
    # Check that all colors start with '#' (are hexadecimal)
    assert all(color.startswith("#") for color in colors)
    # check that all colors are different
    assert len(set(colors)) == len(colors)


def test_hsl_to_hex():
    # Test conversion of HSL to HEX
    # my tests have shown that these conversions don't exactly match online converter tools that I found, but
    # they are very close (and I'm not sure who is right)
    assert hsl_to_hex(0.5, 0.8, 0.4) == "#14b7b7"  # Example values for HSL
    assert hsl_to_hex(0.25, 1, 0.5) == "#7fff00"
