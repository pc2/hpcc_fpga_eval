import pandas as pd

df = pd.read_csv("parsed_watts.csv", header=None, names=['Socket0', 'RAM0', 'Socket1', 'RAM1'])

df["Sum"] = df["Socket0"] + df["RAM0"] + df["Socket1"]+ df["RAM1"]

print(df.head())
print("Average:", df["Sum"].mean())
print("Max:", df["Sum"].max())
