import json

with open('q-extract-nested-json-keys.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('Top-level type:', type(data))
if isinstance(data, list):
    print('First element type:', type(data[0]))
    if isinstance(data[0], dict):
        print('Keys of first element:', list(data[0].keys()))
    else:
        print('First element:', data[0])
elif isinstance(data, dict):
    print('Top-level keys:', list(data.keys()))
else:
    print('Data:', data) 