import sys
import time
from databricks_api import DatabricksAPI
from datetime import datetime, timedelta

print(sys.argv)
token = sys.argv[1]

# Provide a host and token
db = DatabricksAPI(
    host="eastus.azuredatabricks.net",
    token=token
)

job = db.jobs.run_now(
    job_id=1
)