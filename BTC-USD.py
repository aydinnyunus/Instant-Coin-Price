from binance.client import Client
from datetime import datetime
import csv

api_key = "YOUR API KEY"
api_secret = "YOUR API SECRET"
client = Client(api_key, api_secret)

# get market depth
depth = client.get_order_book(symbol='BTCUSDT')

# place a test market buy order, to place an actual order use the create_order function
order = client.create_test_order(
    symbol='BTCUSDT',
    side=Client.SIDE_BUY,
    type=Client.ORDER_TYPE_MARKET,
    quantity=100)

# get all symbol prices
prices = client.get_all_tickers()

# withdraw 100 ETH
# check docs for assumptions around withdrawals
from binance.exceptions import BinanceAPIException, BinanceWithdrawException

try:
    result = client.withdraw(
        asset='BTC',
        address='<btc_address>',
        amount=100)
except BinanceAPIException as e:
    print(e)
except BinanceWithdrawException as e:
    print(e)
else:
    print("Success")

# fetch list of withdrawals
withdraws = client.get_withdraw_history()

# fetch list of ETH withdrawals
eth_withdraws = client.get_withdraw_history(asset='BTC')

# get a deposit address for BTC
address = client.get_deposit_address(asset='USDT')


# start aggregated trade websocket for BNBBTC
def process_message(msg):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    with open('BTCUSD.csv', mode='a') as csv_file:
        fieldnames = ['CryptoCoin', 'Price', 'Date']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'CryptoCoin': 'BitCoin', 'Price': msg, 'Date': dt_string})
    print("message type: {}".format(msg['e']))
    print(msg)
    # do something


from binance.websockets import BinanceSocketManager

bm = BinanceSocketManager(client)
bm.start_aggtrade_socket('BTCUSDT', process_message)
bm.start()

# get historical kline data from any date range

klines = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_1MINUTE, "now UTC")


