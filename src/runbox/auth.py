import datetime as dt
import os
import sys
from pathlib import Path

from garminconnect import Garmin, GarminConnectAuthenticationError
from garth.exc import GarthHTTPError

TOKENSTORE = os.getenv("GARTH_HOME", str(Path.home() / ".garth"))


def connect() -> Garmin:
    """
    Connect to Garmin Connect and return the client. Tokens are generally
    valid for one year.
    """
    try:
        garmin = Garmin()
        garmin.login(TOKENSTORE)

        print(
            f"Successfully connected to Garmin Connect using tokens stored in {TOKENSTORE}"
        )

        return garmin

    except FileNotFoundError:
        print(f"No authentication tokens found at {TOKENSTORE}")
        sys.exit("Stopping.")

    except (GarthHTTPError, GarminConnectAuthenticationError):
        print("The login tokens are invalid or expired. Please rotate them.")
        sys.exit("Stpping.")


def request_data(from_date: dt.date, to_date: dt.date) -> list[dict | None]:
    """
    Request the running activity data from Garmin Connect.
    """

    garmin = connect()

    try:
        # input dates need to be in format '2025-07-22' - if not, the
        # API request will fail and the error cannot be discerned from an autentication error
        activities = garmin.get_activities_by_date(
            from_date.isoformat(), to_date.isoformat(), activitytype="running"
        )
        print(
            f"Fetched {len(activities)} running activities in year {from_date.year}"
            f" from Garmin Connect."
        )

        return activities

    except (GarthHTTPError, GarminConnectAuthenticationError) as err:
        print(err)
        sys.exit(
            "We could not connect to Garmin. The login tokens may be invalid "
            "or expired. Stopping the program."
        )
