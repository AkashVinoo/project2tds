import re
from datetime import datetime

count = 0
with open('s-anand.net-May-2024', encoding='latin-1') as f:
    for line in f:
        # Only process lines with /tamilmp3/
        if '/tamilmp3/' not in line:
            continue
        # Extract date/time
        m = re.search(r'\[([^\]]+)\]', line)
        if not m:
            continue
        dt_str = m.group(1)  # e.g. 30/Apr/2024:07:16:32 -0500
        try:
            dt = datetime.strptime(dt_str.split()[0], "%d/%b/%Y:%H:%M:%S")
        except Exception:
            continue

        # Check if Friday (weekday() == 4)
        if dt.weekday() != 4:
            continue

        # Check time between 03:00 and 19:59
        if not (3 <= dt.hour < 20):
            continue

        # Extract request and status
        req_m = re.search(r'"(GET) (/tamilmp3/[^ ]*) HTTP/[^\"]+" (\d{3}) ', line)
        if not req_m:
            continue
        method, url, status = req_m.groups()
        status = int(status)
        if method == "GET" and 200 <= status < 300:
            count += 1

print(count) 