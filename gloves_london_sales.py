import json
from collections import defaultdict
from metaphone import doublemetaphone

with open('q-clean-up-sales-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('Sample data:')
for entry in data[:5]:
    print(entry)

# Filter for Gloves and sales >= 21
gloves = [entry for entry in data if entry.get('product','').strip().lower() == 'gloves' and int(entry.get('sales',0)) >= 21]

print('\nAll city names and their phonetic keys (from Gloves entries with sales >=21):')
city_set = set()
for entry in gloves:
    city = entry.get('city','').strip()
    key = doublemetaphone(city)[0]
    city_set.add((city, key))
for city, key in sorted(city_set):
    print(f'{city!r} -> {key!r}')

print('\nAll Gloves entries with sales >= 21:')
for entry in gloves:
    print(f"City: {entry.get('city','')}, Sales: {entry.get('sales','')}, Product: {entry.get('product','')}")

# Phonetic clustering of city names
city_clusters = defaultdict(list)
city_phonetic_map = {}
for entry in gloves:
    city = entry.get('city','').strip()
    key = doublemetaphone(city)[0]
    city_clusters[key].append(entry)
    city_phonetic_map[city] = key

# Find the cluster for London (including mis-spellings)
london_key = doublemetaphone('London')[0]
london_sales = sum(int(e['sales']) for e in city_clusters[london_key])

print(f'\nTotal sales for London cluster: {london_sales}') 