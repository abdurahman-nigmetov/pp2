from datetime import datetime, timedelta

def parse_date(line):
    date, time = line.split()
    date = datetime.strptime(date, '%Y-%m-%d')
    utc_sign = 1
    if time[3] == "-":
        utc_sign = -1
    hours = int(time[4:6])
    minutes = int(time[7:9])

    offset = timedelta(hours=hours, minutes=minutes)
    return date - utc_sign * offset

line1 = input()
line2 = input()

date1 = parse_date(line1)
date2 = parse_date(line2)

absolute_time = abs((date1 - date2).total_seconds())
print(int(absolute_time // 86400))