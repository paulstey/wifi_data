import pandas as pd

df_raw = pd.read_csv("/data/wifi-analysis/competition/train.csv")

df = df_raw
df["key"] = 1

pd.set_option('display.width', 100)
df.head(20)

dfc = pd.merge(df_raw, df, on = "key")
