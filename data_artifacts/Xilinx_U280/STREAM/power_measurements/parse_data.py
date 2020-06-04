import pandas as pd

print("DDR:")
df = pd.read_csv("stream_n100_ddr.csv", header=None, names=['12v_pex_mv', '12v_pex_ma', '12v_aux_mv', '12v_aux_ma'], usecols=range(4))

df["Sum"] = (df["12v_pex_mv"]/1000 * df["12v_pex_ma"]/1000) + (df["12v_aux_mv"]/1000 * df["12v_aux_ma"]/1000)

print(df.head())
print("Average:", df["Sum"].mean())
print("Max:", df["Sum"].max())


print("HBM:")
df = pd.read_csv("stream_n100_hbm.csv", header=None, names=['12v_pex_mv', '12v_pex_ma', '12v_aux_mv', '12v_aux_ma'], usecols=range(4))

df["Sum"] = (df["12v_pex_mv"]/1000 * df["12v_pex_ma"]/1000) + (df["12v_aux_mv"]/1000 * df["12v_aux_ma"]/1000)

print(df.head())
print("Average:", df["Sum"].mean())
print("Max:", df["Sum"].max())
