import re
from datetime import datetime
from collections import defaultdict

ip_bytes = defaultdict(int)
with open('s-anand.net-May-2024', encoding='latin-1') as f:
    for line in f:
        # Only process lines with /kannada/
        if ' /kannada/' not in line:
            continue
        # Extract date/time
        m = re.search(r'\[([^\]]+)\]', line)
        if not m:
            continue
        dt_str = m.group(1)  # e.g. 21/May/2024:12:34:56 -0500
        try:
            dt = datetime.strptime(dt_str.split()[0], "%d/%b/%Y:%H:%M:%S")
        except Exception:
            continue
        # Only keep 2024-05-21
        if not (dt.year == 2024 and dt.month == 5 and dt.day == 21):
            continue
        # Extract IP (first field)
        ip = line.split(' ', 1)[0]
        # Extract request and size
        req_m = re.search(r'"(GET|POST|HEAD|PUT|DELETE|OPTIONS|PATCH) (/kannada/[^ ]*) HTTP/[^\"]+" (\d{3}) (\d+)', line)
        if not req_m:
            continue
        method, url, status, size = req_m.groups()
        try:
            size = int(size)
        except Exception:
            continue
        ip_bytes[ip] += size

if ip_bytes:
    top_ip, max_bytes = max(ip_bytes.items(), key=lambda x: x[1])
    print(max_bytes)
else:
    print(0) 