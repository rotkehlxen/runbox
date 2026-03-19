import datetime as dt
import os
import sys
import traceback
from pathlib import Path

import requests
from garminconnect import Garmin, GarminConnectAuthenticationError
from garth.exc import GarthHTTPError

TOKENSTORE = os.getenv("GARTH_HOME", str(Path.home() / ".garth"))


def connect() -> Garmin:
    """
    Connect to Garmin Connect and return the client, with extended debug logging.
    """
    print("🔍 Starting Garmin Connect authentication...")

    try:
        garmin = Garmin()

        print(f"📂 Attempting login with token store at: {TOKENSTORE}")

        try:
            garmin.login(TOKENSTORE)
        except Exception as auth_error:
            print("\n❌ Authentication failed during token login.")
            print("📄 Error type:", type(auth_error).__name__)
            print("🧵 Traceback:")
            traceback.print_exc()

            # Try extracting HTTP information if available
            if hasattr(auth_error, "response") and isinstance(auth_error.response, requests.Response):
                response = auth_error.response

                print("\n🌐 Garmin API raw error response:")
                print("Status code:", response.status_code)
                print("Headers:")
                for k, v in response.headers.items():
                    print(f"  {k}: {v}")

                try:
                    print("\nResponse body:")
                    print(response.text)
                except Exception:
                    print("Could not decode response body.")

            print("\n⚠️ Tokens may be invalid, expired, or Garmin changed the OAuth flow.")
            sys.exit("Stopping due to authentication failure.")

        print(f"✅ Successfully connected to Garmin Connect using tokens stored in {TOKENSTORE}")
        return garmin

    except FileNotFoundError:
        print(f"❌ No authentication tokens found at {TOKENSTORE}")
        sys.exit("Stopping — token file missing.")

    except (GarthHTTPError, GarminConnectAuthenticationError) as e:
        print("\n❌ Garmin API returned an authentication or HTTP error.")
        print("Error:", repr(e))

        if hasattr(e, "response") and isinstance(e.response, requests.Response):
            print("\n🌐 Garmin API response details:")
            print("Status:", e.response.status_code)
            print("Headers:", e.response.headers)
            print("Body:", e.response.text)

        print("\n⚠️ Login tokens invalid or Garmin backend changed behavior.")
        sys.exit("Stopping.")


def request_data(from_date: dt.date, to_date: dt.date) -> list[dict | None]:
    """
    Request the running activity data from Garmin Connect.
    """

    garmin = connect()

    try:
        # input dates need to be in format '2025-07-22' - if not, the
        # API request will fail and the error cannot be discerned from an autentication error
        activities = garmin.get_activities_by_date(from_date.isoformat(), to_date.isoformat(), activitytype="running")
        print(f"Fetched {len(activities)} running activities in year {from_date.year} from Garmin Connect.")

        return activities

    except (GarthHTTPError, GarminConnectAuthenticationError) as err:
        print(err)
        sys.exit("We could not connect to Garmin. The login tokens may be invalid or expired. Stopping the program.")
