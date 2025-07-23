Fetch my Garmin run activity data and visualise them in Github style.

You can find the chart here:
[https://rotkehlxen.github.io/runbox/](https://rotkehlxen.github.io/runbox/)

Github actions are configured to

1. fetch my run activity data from the Garmin Connect API **daily at 9am UTC**
2. update the chart
3. deploy the chart to githup pages (from a dedicated gh-pages branch)

An update of the data/chart can also be triggered manually anytime.

Notes
======

Garmin API access tokens have been created like so:

```python
import garminconnect
import os
from getpass import getpass

email = input("Enter email address: ")
password = getpass("Enter password: ")

garmin = garminconnect.Garmin(email, password)
garmin.login()

GARTH_HOME = os.getenv("GARTH_HOME", "~/.garth")
garmin.garth.dump(GARTH_HOME)
``` 

The tokens (two json files, oauth1_token.json and oauth2_token.json) are dumped to folder `.garth` in the home folder.
To use these tokens in github actions, the json files need to be encoded as strings, e.g.

```bash
cat oauth1_token.json | base64 -w 0
```

Then you can store these strings as Github Secrets. 
Within github actions you can read these strings from the Secrets, decode them using `base64 -d` and write
them back into json files with their orgininal names (check update-chart.yml).
