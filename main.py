import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", None)

# ticker = yf.Ticker('CH0512157782')
#
# df = ticker.history(period="max", auto_adjust=True)

empty_df = pd.read_parquet("stock_data.parquet")

portfolio = pd.DataFrame({"ISIN": [
    "CH0139101593",
    "IE00BYVTMT69",
    "IE00B8J37J31",
    "CH0237935652",
    "CH0012032113",
    "CH0012032113",
    "CH0012005267",
    "CH0000816824",
    "CH0024608827",
    "LU1287022708",
    "AT0000A18XM4",
    "IE00BYWQWR46.SG",
    "US0090661010",
    "CH0512157782"
],
    "Name": [
      "ZKB Gold ETF AA CHF",
       "Invesco Nasdaq-100 UCITS ETF CHF Hedged",
       "iShares MSCI Japan CHF Hedged UCITS ETF",
       "iShares Core SPI® ETF (CH)",
       "Roche Holding AG",
       "Credit Suisse AG",
       "Novartis AG",
       "OC Oerlikon AG",
       "Partners Group AG",
       "Lyxor Pan Africa UCITS ETF", # 19.07.2021
       "ams Osram AG",
       "VanEck Vid Gam USD", # 07.06.2021
       "Arbnb Inc USD",
        "Swisscanto (CH) Institutional Pension Fund III"
    ]
})

empty_df = pd.DataFrame()
for index, row in portfolio.iterrows():
    print(row.ISIN)
    ticker = yf.Ticker(row.ISIN)

    df = ticker.history(period="max", auto_adjust=True)
    df["ISIN"] = row.ISIN
    df["date"] = df.index
    empty_df = pd.concat([empty_df, df])

empty_df.to_parquet("stock_data.parquet", index=False)


empty_df.dtypes
empty_df.groupby("ISIN")["date"].max()

empty_df["close_l1"] = empty_df.groupby("ISIN")["Close"].shift(1)

empty_df["return"] = np.log(empty_df["Close"]/empty_df["close_l1"])


empty_df.groupby("ISIN")["return"].mean()
empty_df.groupby("ISIN")["return"].std()
empty_df.groupby("ISIN")["return"].median()

plt.plot(df['Close'])
plt.show()