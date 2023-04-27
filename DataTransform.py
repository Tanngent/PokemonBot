import pandas as pd

pd.options.display.max_rows = 10

fileList = ["train1.csv","train2.csv"]

df_each = (pd.read_csv(f, keep_default_na=False, header=None, encoding='unicode_escape') for f in fileList)
df = pd.concat(df_each, ignore_index=True)

print(df.shape)