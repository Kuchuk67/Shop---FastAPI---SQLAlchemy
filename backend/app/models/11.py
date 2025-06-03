from datetime import datetime, timezone, timedelta


print(datetime.now())
print(datetime.now(timezone.utc))

print(    datetime.now(timezone(timedelta(hours=3)) )  )