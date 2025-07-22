import os

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
