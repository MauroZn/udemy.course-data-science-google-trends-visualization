import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

def run_challenge(description, func):
    print(f"\nChallenge: {description}")
    input("Press ENTER to see the result...\n")
    func()

df_tesla = pd.read_csv('data/TESLA Search Trend vs Price.csv')
df_btc_search = pd.read_csv('data/Bitcoin Search Trend.csv')
df_btc_price = pd.read_csv('data/Daily Bitcoin Price.csv')
df_unemployment = pd.read_csv('data/UE Benefits Search vs UE Rate 2004-19.csv')

# 1. Basic exploration
def explore_data():
    print(df_tesla.shape)
    print(f'Largest Tesla Web Search: {df_tesla.TSLA_WEB_SEARCH.max()}')
    print(f'Smallest Tesla Web Search: {df_tesla.TSLA_WEB_SEARCH.min()}')
    print(df_tesla.describe())
    print(df_unemployment.shape)
    print(f'Largest Unemployment Web Search: {df_unemployment.UE_BENEFITS_WEB_SEARCH.max()}')
    print(df_btc_price.shape)
    print(df_btc_search.shape)
    print(f'Largest BTC News Search: {df_btc_search.BTC_NEWS_SEARCH.max()}')

# 2. Check missing values
def check_missing():
    print(f'Missing values for Tesla?: {df_tesla.isna().values.any()}')
    print(f'Missing values for U/E?: {df_unemployment.isna().values.any()}')
    print(f'Missing values for BTC Search?: {df_btc_search.isna().values.any()}')
    print(f'Missing values for BTC Price?: {df_btc_price.isna().values.any()}')

# 3. Drop NA
def clean_data():
    df_btc_price.dropna(inplace=True)

# 4. Convert strings to datetime
def convert_dates():
    df_tesla.MONTH = pd.to_datetime(df_tesla.MONTH)
    df_btc_search.MONTH = pd.to_datetime(df_btc_search.MONTH)
    df_unemployment.MONTH = pd.to_datetime(df_unemployment.MONTH)
    df_btc_price.DATE = pd.to_datetime(df_btc_price.DATE)

# 5. Resample BTC price monthly
def resample_btc():
    global df_btc_monthly
    df_btc_monthly = df_btc_price.resample('ME', on='DATE').last()

# 6. Plot Tesla Web Search vs Price
def plot_tesla():
    plt.figure(figsize=(14,8), dpi=120)
    plt.title('Tesla Web Search vs Price', fontsize=18)
    plt.xticks(fontsize=14, rotation=45)

    ax1 = plt.gca()
    ax2 = ax1.twinx()

    ax1.xaxis.set_major_locator(mdates.YearLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax1.xaxis.set_minor_locator(mdates.MonthLocator())

    ax1.set_ylabel('TSLA Stock Price', color='#E6232E', fontsize=14)
    ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

    ax1.set_ylim([0, 600])
    ax1.set_xlim([df_tesla.MONTH.min(), df_tesla.MONTH.max()])

    ax1.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE, color='#E6232E', linewidth=3)
    ax2.plot(df_tesla.MONTH, df_tesla.TSLA_WEB_SEARCH, color='skyblue', linewidth=3)

    plt.show()

# 7. Plot Bitcoin News Search vs Resampled Price
def plot_bitcoin():
    plt.figure(figsize=(14,8), dpi=120)
    plt.title('Bitcoin News Search vs Resampled Price', fontsize=18)
    plt.xticks(fontsize=14, rotation=45)

    ax1 = plt.gca()
    ax2 = ax1.twinx()

    ax1.set_ylabel('BTC Price', color='#F08F2E', fontsize=14)
    ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

    ax1.xaxis.set_major_locator(mdates.YearLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax1.xaxis.set_minor_locator(mdates.MonthLocator())

    ax1.set_ylim(bottom=0, top=15000)
    ax1.set_xlim([df_btc_monthly.index.min(), df_btc_monthly.index.max()])

    ax1.plot(df_btc_monthly.index, df_btc_monthly.CLOSE, color='#F08F2E', linewidth=3, linestyle='--')
    ax2.plot(df_btc_monthly.index, df_btc_search.BTC_NEWS_SEARCH, color='skyblue', linewidth=3, marker='o')

    plt.show()

# 8. Plot Unemployment Benefits vs U/E Rate
def plot_unemployment():
    plt.figure(figsize=(14,8), dpi=120)
    plt.title('Monthly Search of "Unemployment Benefits" vs U/E Rate', fontsize=18)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14, rotation=45)

    ax1 = plt.gca()
    ax2 = ax1.twinx()

    ax1.set_ylabel('FRED U/E Rate', color='purple', fontsize=14)
    ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

    ax1.xaxis.set_major_locator(mdates.YearLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax1.xaxis.set_minor_locator(mdates.MonthLocator())

    ax1.set_ylim(bottom=3, top=10.5)
    ax1.set_xlim([df_unemployment.MONTH.min(), df_unemployment.MONTH.max()])
    ax1.grid(color='grey', linestyle='--')

    ax1.plot(df_unemployment.MONTH, df_unemployment.UNRATE, color='purple', linewidth=3, linestyle='--')
    ax2.plot(df_unemployment.MONTH, df_unemployment.UE_BENEFITS_WEB_SEARCH, color='skyblue', linewidth=3)

    plt.show()

# 9. Rolling average plot
def plot_rolling_avg():
    roll_df = df_unemployment[['UE_BENEFITS_WEB_SEARCH', 'UNRATE']].rolling(window=6).mean()

    plt.figure(figsize=(14,8), dpi=120)
    plt.title('Rolling Monthly "Unemployment Benefits" Web Searches vs UNRATE', fontsize=18)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14, rotation=45)

    ax1 = plt.gca()
    ax2 = ax1.twinx()

    ax1.xaxis.set_major_locator(mdates.YearLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax1.xaxis.set_minor_locator(mdates.MonthLocator())

    ax1.set_ylabel('FRED U/E Rate', color='purple', fontsize=16)
    ax2.set_ylabel('Search Trend', color='skyblue', fontsize=16)

    ax1.set_ylim(bottom=3, top=10.5)
    ax1.set_xlim([df_unemployment.MONTH[0], df_unemployment.MONTH.max()])

    ax1.plot(df_unemployment.MONTH, roll_df.UNRATE, 'purple', linewidth=3, linestyle='-.')
    ax2.plot(df_unemployment.MONTH, roll_df.UE_BENEFITS_WEB_SEARCH, 'skyblue', linewidth=3)

    plt.show()

# 10. Plot 2020 data
def plot_2020():
    df_ue_2020 = pd.read_csv('data/UE Benefits Search vs UE Rate 2004-20.csv')
    df_ue_2020.MONTH = pd.to_datetime(df_ue_2020.MONTH)

    plt.figure(figsize=(14,8), dpi=120)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14, rotation=45)
    plt.title('Monthly "Unemployment Benefits" Web Search vs UNRATE incl. 2020', fontsize=18)

    ax1 = plt.gca()
    ax2 = ax1.twinx()

    ax1.set_ylabel('FRED U/E Rate', color='purple', fontsize=16)
    ax2.set_ylabel('Search Trend', color='skyblue', fontsize=16)

    ax1.set_xlim([df_ue_2020.MONTH.min(), df_ue_2020.MONTH.max()])
    ax1.plot(df_ue_2020.MONTH, df_ue_2020.UNRATE, 'purple', linewidth=3)
    ax2.plot(df_ue_2020.MONTH, df_ue_2020.UE_BENEFITS_WEB_SEARCH, 'skyblue', linewidth=3)

    plt.show()


# ------------------ Run Challenges ------------------------------------------------------------------------------------

run_challenge("Explore datasets and summary statistics", explore_data)

run_challenge("Check for missing values", check_missing)

run_challenge("Clean Bitcoin price data (drop NA)", clean_data)

run_challenge("Convert date columns to datetime", convert_dates)

run_challenge("Resample BTC price monthly", resample_btc)

run_challenge("Plot Tesla Web Search vs Stock Price", plot_tesla)

run_challenge("Plot Bitcoin News Search vs Price", plot_bitcoin)

run_challenge("Plot Unemployment Web Search vs Unemployment Rate", plot_unemployment)

run_challenge("Plot 6-month rolling average of UE search + rate", plot_rolling_avg)

run_challenge("Plot updated 2020 unemployment data", plot_2020)

