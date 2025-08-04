import pandas as pd
import numpy as np

def main():
    df = pd.read_excel('q-clean-up-excel-sales-data.xlsx')
    # Trim and normalize strings
    df['Customer Name'] = df['Customer Name'].astype(str).str.strip()
    df['Country'] = df['Country'].astype(str).str.strip().str.upper()
    country_map = {
        'USA': 'US', 'U.S.A': 'US', 'US': 'US', 'UNITED STATES': 'US',
        'UAE': 'AE', 'U.A.E': 'AE', 'AE': 'AE', 'UNITED ARAB EMIRATES': 'AE',
        'UK': 'GB', 'U.K': 'GB', 'UNITED KINGDOM': 'GB',
        'BR': 'BR', 'BRA': 'BR', 'BRAZIL': 'BR', 'BRASIL': 'BR',
        'FRA': 'FR', 'FRANCE': 'FR', 'FR': 'FR',
        'IND': 'IN', 'INDIA': 'IN',
    }
    df['Country'] = df['Country'].replace(country_map)
    # Standardize date formats
    def parse_date(x):
        x = str(x).strip()
        for fmt in (
            '%m-%d-%Y', '%Y/%m/%d', '%Y-%m-%d', '%d-%b-%Y', '%d/%m/%Y', '%d-%m-%Y',
            '%b %d, %Y', '%d %b %Y', '%a %b %d %Y %H:%M:%S GMT%z (%Z)'
        ):
            try:
                return pd.to_datetime(x, format=fmt)
            except:
                continue
        try:
            return pd.to_datetime(x)
        except:
            return pd.NaT
    df['Date'] = df['Date'].apply(parse_date)
    # Extract product name
    df['Product'] = df['Product/Code'].astype(str).str.split('/').str[0].str.strip()
    # Clean and convert Sales/Cost
    df['Sales'] = df['Sales'].astype(str).str.replace('USD','').str.replace(',','').str.strip()
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
    df['Cost'] = df['Cost'].astype(str).str.replace('USD','').str.replace(',','').str.strip()
    df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
    df['Cost'] = df.apply(lambda row: row['Sales']*0.5 if np.isnan(row['Cost']) else row['Cost'], axis=1)
    # Print unique values for debugging
    print('Unique Product values:', df['Product'].unique())
    print('Unique Country values:', df['Country'].unique())
    print('Sample Dates:', df['Date'].dropna().sort_values().unique()[:10])
    # Filter
    cutoff = pd.to_datetime('2023-02-14 19:21:06')
    mask = (df['Date'] <= cutoff) & (df['Product'].str.upper() == 'IOTA') & (df['Country'] == 'BR')
    filtered = df[mask]
    print('\nFiltered transactions for Iota in BR before cutoff:')
    print(filtered[['Date','Product','Country','Sales','Cost']])
    total_sales = filtered['Sales'].sum()
    total_cost = filtered['Cost'].sum()
    margin = (total_sales - total_cost) / total_sales if total_sales else 0
    with open('margin_result.txt', 'w') as f:
        f.write(f'{margin:.6f}\n')

if __name__ == '__main__':
    main() 