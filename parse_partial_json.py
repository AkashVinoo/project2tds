import re

total = 0
lines = []
with open('q-parse-partial-json.jsonl', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i < 20:
            lines.append(line.strip())
        # Find all numbers after '"sales":'
        for match in re.finditer(r'"sales"\s*:\s*([0-9eE.+-]+)', line):
            try:
                total += float(match.group(1))
            except Exception:
                continue
print('Sample lines:')
for l in lines:
    print(l)
print('\nRegex total:', total) 