#!/usr/bin/env python3

# IMPORTS
import pandas as pd
import os.path
from binance.client import Client
import datetime
import argparse


# Utils
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Config:
    source: str
    from_date: datetime.date
    to_date: datetime.date
    symbol: str
    interval: str
    csv_directory: str
    response_format: str
    in_timestamp: bool


# Functions
def binance(config):
    api_key = os.environ.get("BINANCE_API_KEY")
    api_secret = os.environ.get("BINANCE_API_SECRET")

    if api_key is None or api_key == "":
        raise Exception("missing the binance api key")
    if api_secret is None or api_secret == "":
        raise Exception("missing the binance api secret")

    client = Client(api_key=api_key, api_secret=api_secret)
    fetch_binance_klines(client, config.from_date, config.to_date, config.symbol, config.interval,
                         config.csv_directory, config.response_format, config.in_timestamp)


def fetch_binance_klines(client, from_date, to_date, symbol, interval, csv_dir, response_format, in_timestamp):
    date_filename = '%s-to-%s' % (from_date.strftime("%d-%b-%Y"), to_date.strftime("%d-%b-%Y"))
    filename = '%s/%s-%s-%s.csv' % (csv_dir, symbol, interval, date_filename)

    if os.path.isfile(filename):
        file = open(filename, "w")
        file.close()
    print(Colors.OKBLUE + 'Downloading %s dataset for %s from %s to %s. Be patient...'
          % (interval, symbol, from_date, to_date) + Colors.ENDC)
    klines = client.get_historical_klines(symbol, interval, from_date.strftime("%d %b %Y %H:%M:%S"),
                                          to_date.strftime("%d %b %Y %H:%M:%S"))
    data = pd.DataFrame(klines,
                        columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av',
                                 'trades', 'tb_base_av', 'tb_quote_av',
                                 'ignore'])  # tb -> Taker buy, av -> asset volume
    if in_timestamp is False:
        data['open_time'] = pd.to_datetime(data['open_time'], unit='ms')

    if response_format == "short":
        # Delete columns to make the file lighter
        data.drop('close_time', axis=1, inplace=True)
        data.drop('quote_av', axis=1, inplace=True)
        data.drop('tb_base_av', axis=1, inplace=True)
        data.drop('tb_quote_av', axis=1, inplace=True)
        data.drop('ignore', axis=1, inplace=True)

    df = data
    print(df.to_string(max_rows=10))
    df.set_index('open_time', inplace=True)
    df.to_csv(filename)
    print(Colors.OKGREEN + 'File downloaded and successfully written in %s' % filename + Colors.ENDC)
    return df


def main():
    p = argparse.ArgumentParser(description="Fetch historical data and save it in a csv file")
    p.add_argument("--source",
                   required=False,
                   type=str,
                   default="binance",
                   help="specifies the data provider (binance)")
    p.add_argument("--from-date",
                   dest="from_date",
                   required=False,
                   type=lambda d: datetime.datetime.strptime(d, '%d/%m/%Y %H:%M:%S').date(),
                   help="from date (DD/MM/YYYY HH:MM:SS)",
                   default=datetime.datetime.now() - datetime.timedelta(days=200))
    p.add_argument("--to-date",
                   dest="to_date",
                   required=False,
                   type=lambda d: datetime.datetime.strptime(d, '%d/%m/%Y %H:%M:%S').date(),
                   help="to date (DD/MM/YYYY HH:MM:SS)",
                   default=datetime.datetime.now())
    p.add_argument("-s", "--symbol", required=True, type=str, help="symbol (e.g. BTCUSDT)")
    p.add_argument("-i", "--interval",
                   required=False,
                   type=str,
                   help="interval (1m|3m|5m|15m|30m|1h|2h|4h|6h|8h|12h|1d|3d|1w|1M)",
                   default="1m")
    p.add_argument("--dir",
                   dest="csv_directory",
                   required=False,
                   type=str,
                   help="destination directory of the csv file",
                   default="dataset")
    p.add_argument("--format",
                   dest="response_format",
                   required=False,
                   type=str,
                   default="short",
                   help="response format of the candlestick (short|full)")
    p.add_argument("--timestamp",
                   dest="in_timestamp",
                   required=False,
                   type=bool,
                   default=True,
                   help="keep the date in timestamp")

    args = p.parse_args()
    config = Config()

    config.source = args.source
    config.from_date = args.from_date
    config.to_date = args.to_date
    config.symbol = args.symbol
    config.interval = args.interval
    config.csv_directory = args.csv_directory
    config.response_format = args.response_format
    config.in_timestamp = args.in_timestamp

    if args.source == "binance":
        binance(config)
    else:
        raise Exception("unsupported data provider")


if __name__ == "__main__":
    main()
