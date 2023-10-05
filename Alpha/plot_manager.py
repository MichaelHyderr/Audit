import pandas as pd

df = pd.read_csv("Priority_Table.csv")

print(df["Priority"].max())
print(df["Priority"].idxmax())
print(df["KSS"][127])
print(df.loc[127])

print(df.sort_values("Priority", ascending=False))


serie1 = df.groupby("KSA")["KSA Points"].first()
#  testato su colab