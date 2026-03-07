from datetime import datetime, timezone, timedelta

def parse_line(s):
    date_part, time_part, tz_part = s.strip().split()
    y, m, d = map(int, date_part.split("-"))
    hh, mm, ss = map(int, time_part.split(":"))
    sign = 1 if tz_part[3] == "+" else -1
    tzh, tzm = map(int, tz_part[4:].split(":"))
    offset = sign * (tzh * 60 + tzm)
    tz = timezone(timedelta(minutes=offset))
    return datetime(y, m, d, hh, mm, ss, tzinfo=tz)

start = parse_line(input().strip())
end = parse_line(input().strip())

start_utc = start.astimezone(timezone.utc)
end_utc = end.astimezone(timezone.utc)

print(int((end_utc - start_utc).total_seconds()))