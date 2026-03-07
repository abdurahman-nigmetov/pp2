from datetime import datetime, timezone, timedelta

def parse_line(s):
    date_part, tz_part = s.strip().split()
    y, m, d = map(int, date_part.split("-"))
    sign = 1 if tz_part[3] == "+" else -1
    hh, mm = map(int, tz_part[4:].split(":"))
    offset_minutes = sign * (hh * 60 + mm)
    tz = timezone(timedelta(minutes=offset_minutes))
    return y, m, d, tz

def is_leap(year):
    return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)

def birthday_date_for_year(year, bm, bd):
    if bm == 2 and bd == 29 and not is_leap(year):
        return year, 2, 28
    return year, bm, bd

b_line = input().strip()
c_line = input().strip()

by, bm, bd, btz = parse_line(b_line)
cy, cm, cd, ctz = parse_line(c_line)

current_local = datetime(cy, cm, cd, 0, 0, 0, tzinfo=ctz)
current_utc = current_local.astimezone(timezone.utc)

for target_year in (cy, cy + 1):
    ty, tm, td = birthday_date_for_year(target_year, bm, bd)
    bday_local = datetime(ty, tm, td, 0, 0, 0, tzinfo=btz)
    bday_utc = bday_local.astimezone(timezone.utc)
    if bday_utc >= current_utc:
        delta_seconds = int((bday_utc - current_utc).total_seconds())
        print(delta_seconds // 86400)
        break