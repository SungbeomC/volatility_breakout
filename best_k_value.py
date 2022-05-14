import pandas as pd
import numpy as np

firm = "AAPL"
fileName = "./Data/" + firm + ".csv"
df = pd.read_csv(fileName, sep=",", header=0)

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values(by="Date", ascending=True)

for column in ["Close/Last", "Open", "High", "Low"]:
    df[column] = df[column].str.replace("$", "", regex=False).astype(float)

df["MA10"] = df["Close/Last"].rolling(window=10).mean()

for k in np.arange(0.0, 1.0, 0.1):
    k = round(k, 2)
    df["Range"] = (df["High"] - df["Low"]) * k
    df["Target"] = df["Open"] + df["Range"].shift(1)

    df[firm + "_ror_MA"] = np.where((df["High"] > df["Target"]) & (df["Open"] > df["MA10"]),
                                    df["Close/Last"] / df["Target"], 1)
    df[firm + "_hpr_MA"] = df[firm + "_ror_MA"].cumprod()

    ror = np.around(df[firm + "_hpr_MA"].max(), 4)
    print("When k =", str(k) + ",", "the rate of return is " + str(ror))
