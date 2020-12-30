# crypto-historical-data

Fetch historical data from the exchange platform and save it in a csv file.

## Supported exchange
- Binance

## Install

### Activating Virtualenv

`python3 -m venv env`

On Unix or MacOS, run:

`source env/bin/activate`

On Windows, run:

`env\Scripts\activate.bat`

### Installing dependencies

`pip install -r requirements.txt`

### Add API

#### Binance

To get your API:
https://www.binance.com/en/support/faq/360002502072-How-to-create-API

Add your API to your environment:

`export BINANCE_API_KEY=YOUR_API_KEY`

`export BINANCE_API_SECRET=YOUR_API_SECRET`

## Usage

Run `./historical_data.py -h` for more information.

For example run:
 
`./historical_data.py -s BTCUSDT --from-date "18/12/2020 00:00:00" --to-date "20/12/2020 00:00:00" -i 1m --format short`

This will fetch candlesticks data from 18/12/2020 00:00:00
to the 20/12/2020 00:00:00 of the BTCUSDT symbol with a 1 minute interval.
The csv file is located in the `dataset` directory by default.
The short format will display only the minimum necessary to preserve the file size.