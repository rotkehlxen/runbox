import datetime as dt
import os
import sys

from garminconnect import Garmin, GarminConnectAuthenticationError
from garth.exc import GarthHTTPError

TOKENSTORE = os.getenv("GARTH_HOME", "~/.garth")


def connect() -> Garmin | None:
    """
    Connect to Garmin Connect and return the client. Tokens are generally
    valid for one year.
    """
    try:
        garmin = Garmin()
        garmin.login(TOKENSTORE)

        return garmin

    except FileNotFoundError:
        print(f"No authentication tokens found at {TOKENSTORE}")

    except (GarthHTTPError, GarminConnectAuthenticationError):
        print("The login tokens are invalid or expired. Please rotate them.")


def request_data(from_date: dt.date, to_date: dt.date) -> list[dict | None]:
    """
    Request the activity data from Garmin Connect.
    """

    garmin = connect()

    if garmin:
        try:
            activities = garmin.get_activities_by_date(
                from_date.isoformat(), to_date.isoformat
            )

            return activities

        except (GarthHTTPError, GarminConnectAuthenticationError):
            print("The login tokens are invalid or expired. Please rotate them.")

    else:
        sys.exit("We could not connect to Grarmin. Stopping the program.")
