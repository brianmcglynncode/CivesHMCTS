import pandas as pd
import sys

# Set encoding to utf-8 for stdout if possible, but we will also manually sanitize
sys.stdout.reconfigure(encoding='utf-8')

try:
    df = pd.read_excel('MH 3.xlsx', header=None)
    print(f"Shape: {df.shape}")
    
    # Print first 10 rows, replacing non-ascii with ?
    for i in range(min(10, len(df))):
        row = df.iloc[i]
        safe_values = []
        for val in row:
            s_val = str(val)
            s_val = s_val.encode('ascii', 'replace').decode('ascii')
            safe_values.append(s_val)
        print(f"Row {i}: {safe_values}")

except Exception as e:
    print(f"Error: {e}")
