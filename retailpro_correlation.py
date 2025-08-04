import sqlite3
import pandas as pd
import json

# 1. Load the SQL file into SQLite
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
with open('q-sql-correlation-github-pages.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()
cursor.executescript(sql_script)

# 2. Find the table name and relevant columns
# We'll try to find a table with columns Avg_Basket, Net_Sales, Promo_Spend
query = """
SELECT name FROM sqlite_master WHERE type='table';
"""
tables = [row[0] for row in cursor.execute(query)]
found = False
for table in tables:
    cols = [row[1] for row in cursor.execute(f"PRAGMA table_info({table})").fetchall()]
    if all(col in cols for col in ['Avg_Basket', 'Net_Sales', 'Promo_Spend']):
        df = pd.read_sql_query(f"SELECT Avg_Basket, Net_Sales, Promo_Spend FROM {table}", conn)
        found = True
        break
if not found:
    raise Exception('No table with required columns found.')

# 3. Calculate correlations
corrs = {}
corrs['Avg_Basket-Net_Sales'] = df['Avg_Basket'].corr(df['Net_Sales'])
corrs['Avg_Basket-Promo_Spend'] = df['Avg_Basket'].corr(df['Promo_Spend'])
corrs['Net_Sales-Promo_Spend'] = df['Net_Sales'].corr(df['Promo_Spend'])

# 4. Find the strongest correlation (by absolute value)
pair, corr = max(corrs.items(), key=lambda x: abs(x[1]))

# 5. Output as JSON
result = {"pair": pair, "correlation": corr}
with open('retailpro_correlation.json', 'w') as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2)) 