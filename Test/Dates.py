from datetime import date
from datetime import timedelta

today = date.today()
print("Today is: ",today)

yesterday = today - timedelta(days = 1)
print("Yesterday was: ",yesterday)
