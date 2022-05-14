import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl

firm = "AMZN"
fileName = "./Data/" + firm + ".csv"
df = pd.read_csv(fileName, sep=",", header=0)

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values(by="Date", ascending=True)

for column in ["Close/Last", "Open", "High", "Low"]:
    df[column] = df[column].str.replace("$", "", regex=False).astype(float)

df["MA10"] = df["Close/Last"].rolling(window=10).mean()

k = 0.5  # Set the value of k to 0.5 (K value might change according to any change in market flow and other factors)
df["Range"] = (df["High"] - df["Low"]) * k
df["Target"] = df["Open"] + df["Range"].shift(1)

df[firm + "_ror"] = np.where((df["High"] > df["Target"]), df["Close/Last"] / df["Target"], 1)
df[firm + "_hpr"] = df[firm + "_ror"].cumprod()
df[firm + "_dd"] = (df[firm + "_hpr"].cummax() - df[firm + "_hpr"]) / df[firm + "_hpr"].cummax() * 100
mdd = np.around(df[firm + "_dd"].max(), 4)
print(firm + "_MDD(%):", mdd)

df[firm + "_ror_MA"] = np.where((df["High"] > df["Target"]) & (df["Open"] > df["MA10"]),
                                df["Close/Last"] / df["Target"], 1)
df[firm + "_hpr_MA"] = df[firm + "_ror_MA"].cumprod()
df[firm + "_dd_MA"] = (df[firm + "_hpr_MA"].cummax() - df[firm + "_hpr_MA"]) / df[firm + "_hpr_MA"].cummax() * 100
mdd_MA = np.around(df[firm + "_dd_MA"].max(), 4)
print(firm + "_MDD(%)_MA:", mdd_MA)

df.to_csv("backtest_Amazon.csv", index=False)
df.to_excel("backtest_Amazon.xlsx")

# Use graphs to visualize how different percentages of return are according to whether the volatility breakout strategy
# includes the moving average (MA) as a determinant to buy a certain stock

fig = plt.figure(figsize=(14, 6))
ax = fig.add_subplot(1, 1, 1)
ax.plot(df["Date"], df[firm + "_hpr"], label="VB")
ax.plot(df["Date"], df[firm + "_hpr_MA"], label="VB + MA")

plt.title("Amazon")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.grid(True, axis='y')
plt.legend()
plt.show()

# Use graphs to visualize how different percentages of drawdown are according to whether the volatility breakout
# strategy includes the moving average (MA) as a determinant to buy a certain stock

fig = plt.figure(figsize=(14, 6))
ax = fig.add_subplot(1, 1, 1)

ax.plot(df["Date"], df[firm + "_dd"] * -1, label="VB")
ax.plot(df["Date"], df[firm + "_dd_MA"] * -1, label="VB + MA")

ax.grid()
plt.title("Amazon")
plt.xlabel("Date")
plt.ylabel("Drawdown")
plt.legend(loc="best")
plt.show()
