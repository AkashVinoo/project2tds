import json

def count_key(obj, target):
    count = 0
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == target:
                count += 1
            count += count_key(v, target)
    elif isinstance(obj, list):
        for item in obj:
            count += count_key(item, target)
    return count

with open('q-extract-nested-json-keys.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

result = count_key(data, 'UQCY')
print(result) 