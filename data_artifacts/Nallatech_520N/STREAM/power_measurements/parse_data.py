import pandas as pd

df = pd.read_csv("powermeasure.csv", header=None, names=['watts'])

print(df.head())
print("Average:", df["watts"].mean())
print("Max:", df["watts"].max())

