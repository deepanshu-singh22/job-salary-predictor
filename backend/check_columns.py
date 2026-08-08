import pandas as pd
import config

df = pd.read_csv(config.DATA_PATH)
print("Total columns:", len(df.columns))
print("\nColumn names (exact):")
for col in df.columns:
    print(repr(col))