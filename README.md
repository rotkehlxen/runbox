Fetch my Garmin run activity data and visualise them in Github style.

You can find the chart here:
[https://rotkehlxen.github.io/runbox/](https://rotkehlxen.github.io/runbox/)

Github actions are configured to

1. fetch my run activity data from the Garmin Connect API **every Monday at 7pm UTC**
2. update the chart
3. deploy the chart to githup pages (from a dedicated gh-pages branch)

An update of the data/chart can also be triggered manually anytime.

Notes
======

Garmin API access tokens have been created like so:

```python
import garminconnect
from getpass import getpass

email = input("Enter email address: ")
password = getpass("Enter password: ")

garmin = garminconnect.Garmin(email, password)
garmin.login('~/.garminconnect')
``` 

One token file named `garmin_tokens.json` will be written to folder `˜/.garminconnect`
To use this token in github actions, the json file has to be encoded as a string, e.g.

```bash
cat garmin_tokens.json | base64 -w 0
```

Then you can store this string as a Github Secret. 
Within github actions you can read the string from the Secret, decode it using `base64 -d` and write it back into a json file with its orgininal name (check update-chart.yml for details).
