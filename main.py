from modules.config import PRICE_FILE, EVENT_FILE
from modules.data_loader import load_brent_data
from modules.event_collector import load_event_data
from modules.eda import plot_price_trend, plot_log_returns
from modules.time_series_utils import compute_log_returns, check_stationarity

def main():
    df_prices = load_brent_data(PRICE_FILE)
    df_events = load_event_data(EVENT_FILE)

    plot_price_trend(df_prices)
    plot_log_returns(df_prices)

    log_df = compute_log_returns(df_prices)
    stationarity = check_stationarity(log_df["Log_Return"])
    
    print("ADF Test Result:")
    for key, val in stationarity.items():
        print(f"{key}: {val}")

if __name__ == "__main__":
    main()
