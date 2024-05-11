import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime as dttm
# import asyncio
# import pandas as pd
# import datetime
from random import choice
import math
import decimal
from api_binance import BINANCE_API
from log import log_exceptions_decorator

# def server_to_utc_difference_counter():
#     server_time_naive = dttm.now()
#     print(f"server_time_naive: {server_time_naive}")
#     utc_time = dttm.utcnow()
#     print(f"utc_time: {utc_time}")
#     time_difference = server_time_naive - utc_time
#     total_seconds = abs(time_difference.total_seconds()) * 1000
#     total_seconds = math.ceil(total_seconds)
#     if total_seconds < 10:
#         return 0
#     return total_seconds

# time_correction = server_to_utc_difference_counter()
# print("ms difference:", time_correction)

class UTILS():
    def __init__(self):  
        # super().__init__()
        pass

    @log_exceptions_decorator
    def date_of_the_month(self):        
        current_time = time.time()        
        datetime_object = dttm.fromtimestamp(current_time)       
        formatted_time = datetime_object.strftime('%d')
        return int(formatted_time) 
    
    @log_exceptions_decorator
    def time_calibrator(self, kline_time, time_frame):
        current_time = time.time()
        time_in_seconds = 0

        if time_frame == 'm':
            time_in_seconds = kline_time * 60
        elif time_frame == 'h':
            time_in_seconds = kline_time * 3600
        elif time_frame == 'd':
            time_in_seconds = kline_time * 86400

        next_interval = math.ceil(current_time / time_in_seconds) * time_in_seconds
        wait_time = next_interval - current_time
        return int(wait_time)
    
    @log_exceptions_decorator
    def show_post_trade_info(self, stop_loss_multiplier):
        if stop_loss_multiplier == -1:
            return "The position closed with a loss/Позиция закрыта c убытком"
        elif stop_loss_multiplier == 0:
            return "The position is closed at the breakeven point/Позиция закрыта в точке безубыточности"
        else:
            return f"Position closed with a profit. Trailling multipliter is equal: {stop_loss_multiplier}\n Позиция закрыта c прибылью. Множетель позиции равен {stop_loss_multiplier}"
    
    @log_exceptions_decorator
    def usdt_to_qnt_converter(self, symbol, depo, symbol_info, cur_price):
        qty = None
        symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)
        # //////////////////////
        quantity_precision = int(float(symbol_data['quantityPrecision']))
        print(f"quantity_precision2: {quantity_precision}")
        qty = round(depo / cur_price, quantity_precision)
        # min_qnt = float(symbol_data['filters'][1]['minQty'])
        # print(f"min_qnt: {min_qnt}")
        # max_qnt = float(symbol_data['filters'][1]['maxQty']) 
        # if qty <= min_qnt:
        #     return min_qnt, quantity_precision              
        # elif qty >= max_qnt:
        #     return max_qnt, quantity_precision    
        return qty, quantity_precision

    @log_exceptions_decorator
    def from_anomal_view_to_normal(self, strange_list):
        normal_list = [] 
        # /////////////////////////////////////////////////////
        for x in strange_list:
            x_f = decimal.Decimal(str(x))
            normal_list.append(format(x_f, 'f'))
        print(' '.join(normal_list)) 

class COIN_MARKET_API_PARSER():
    def __init__(self) -> None:
        # super().__init__()
        pass

    def top_coins_engin(self, api_key, limit):
        url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': api_key,
        }
        params = {
            'start': '1',
            'limit': limit,
            'convert': 'USD',  
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            top_coins = data['data']
            return top_coins
        # else:
        #     print(f"Ошибка при запросе данных: {response.status_code}")
        return None
    
    def coin_market_cup_top(self, api_key, limit):
        top_coins_total_list = []
        top_coins = self.top_coins_engin(api_key, limit)
        if top_coins:
            for coin in top_coins:
                try:
                    top_coins_total_list.append(f"{coin['symbol']}USDT")
                except:
                    pass
            return top_coins_total_list
        return

# print(COIN_MARKET_API_PARSER().coin_market_cup_top())
                                    
