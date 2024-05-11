                
            # if 'bb_fib_flag' in current_bunch:     
            #     buy_bband_signal, sell_bband_signal = False, False           
            #     df = self.calculate_bollinger_bands(df)
            #     buy_bband_signal = close_price > df['BBL_30_1.618'].iloc[-1] and close_price < df['BBM_30_1.382'].iloc[-1]
            #     sell_bband_signal = close_price < df['BBU_30_1.618'].iloc[-1] and close_price > df['BBM_30_1.382'].iloc[-1]
            #     signals_sum.append((buy_bband_signal, sell_bband_signal))

            # if 'bb_fib2_doji_pattern_flag' in current_bunch:     
            #     buy_bband_signal, sell_bband_signal = False, False           
            #     df = self.calculate_bollinger_bands(df)
            #     # print(df)
            #     bb_l = df['BBL_30_1.618'].iloc[-1]
            #     bb_u = df['BBU_30_1.618'].iloc[-1]
            #     df = self.calculate_doji(df)
            #     doji = df["Doji"].iloc[-1]
            #     # print(close_price)
            #     # print(doji)
            #     # print(bb_l)
            #     # print(bb_u)
            #     buy_bband_signal = close_price < bb_l and doji == 100
            #     sell_bband_signal = close_price > bb_u and doji == 100
            #     signals_sum.append((buy_bband_signal, sell_bband_signal))  

            # if 'bb_fib_flag' in current_bunch:     
            #     buy_bband_signal, sell_bband_signal = False, False           
            #     df = self.calculate_bollinger_bands(df)
            #     buy_bband_signal = close_price > df['BBL_30_1.618'].iloc[-1] and close_price < df['BBM_30_1.382'].iloc[-1]
            #     sell_bband_signal = close_price < df['BBU_30_1.618'].iloc[-1] and close_price > df['BBM_30_1.382'].iloc[-1]
            #     signals_sum.append((buy_bband_signal, sell_bband_signal))

            # if 'bb_fib2_doji_pattern_flag' in current_bunch:     
            #     buy_bband_signal, sell_bband_signal = False, False           
            #     df = self.calculate_bollinger_bands(df)
            #     # print(df)
            #     bb_l = df['BBL_30_1.618'].iloc[-1]
            #     bb_u = df['BBU_30_1.618'].iloc[-1]
            #     df = self.calculate_doji(df)
            #     doji = df["Doji"].iloc[-1]
            #     # print(close_price)
            #     # print(doji)
            #     # print(bb_l)
            #     # print(bb_u)
            #     buy_bband_signal = close_price < bb_l and doji == 100
            #     sell_bband_signal = close_price > bb_u and doji == 100
            #     signals_sum.append((buy_bband_signal, sell_bband_signal))             
              


            # if 'heikin_ashi_strategy_flag' in current_bunch:
            #     buy_heikin_ashi_signal, sell_heikin_ashi_signal = False, False
            #     df = self.calculate_ema(df)
            #     ema_10, ema_30 = df["EMA10"].iloc[-1], df["EMA30"].iloc[-1]
            #     # print(ema_10, ema_30)
            #     df = self.calculate_doji(df)
            #     doji = df["Doji"].iloc[-1]
            #     # print(doji)
            #     heiken_close, heiken_open, heiken_signal = self.calculate_heikin_ashi(df)
            #     # print(heiken_close, heiken_open, heiken_signal)
            #     buy_heikin_ashi_signal = (ema_10 > ema_30) and (heiken_open < ema_10) and (heiken_close > ema_10) and (heiken_signal == 2) and (doji == 0)
            #     sell_heikin_ashi_signal = (ema_10 < ema_30) and (heiken_open > ema_10) and (heiken_close < ema_10) and (heiken_signal == 1) and (doji == 0)
            #     signals_sum.append((buy_heikin_ashi_signal, sell_heikin_ashi_signal))





        # url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}' # spot

        # response = requests.get(self.URL_PATTERN_DICT["klines_url"])
        # if response.status_code != 200:
        #     print(f'Failed to fetch data. Status code: {response.status_code}')
        #     return pd.DataFrame()
        # data = response.json()
        # data = pd.DataFrame(data, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVolume', 'NumberOfTrades', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume', 'Ignore'])
        # data['Time'] = pd.to_datetime(data['Time'].astype(int), unit='ms')
        # data.set_index('Time', inplace=True)
        # return data.astype(float)




# class DELETEE_API(POSTT_API):
#     ...

    # def cancel_all_orders_for_position(self, symbol_list):
    #     method = 'DELETE'
    #     cancel_orders_list = []      

    #     for item in symbol_list:
    #         cancel_order = None
    #         params = {}
    #         params["symbol"] = item
    #         params = self.get_signature(params)
    #         url = self.URL_PATTERN_DICT['cancel_all_orders_url']
            
    #         cancel_order = self.HTTP_request(url, method=method, headers=self.header, params=params)
    #         cancel_orders_list.append(cancel_order)
            
    #     return cancel_orders_list
    
    # def cancel_all_open_orders(self):
    #     method = 'DELETE'

    #     cancel_orders = None
    #     all_orders = None
    #     all_orders = self.get_all_orders()

    #     for item in all_orders:
    #         params = {}
    #         params["symbol"] = item["symbol"]
    #         params = self.get_signature(params)
    #         url = self.URL_PATTERN_DICT['cancel_all_orders_url']
    #         method = 'DELETE'
    #         cancel_orders = self.HTTP_request(url, method=method, headers=self.header, params=params)
    #         # print(cancel_orders)

    #     return


        # time.sleep(random.randrange(59, 69))



# import websocket
# import time

# def on_message(ws, message):
#     time.sleep(1)
#     print(message)
#     print(f"{last_close_data}")
#     ws.close()

# def on_error(ws, error):
#     print(error)

# def on_close(ws):
#     print("### closed ###")

# def on_open(ws):
#     print("### connected ###")

# def websocket_data():
#     ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/btcusdt@trade")
#     ws.on_message = on_message
#     # ws.on_error = on_error
#     # ws.on_close = on_close
#     # ws.on_open = on_open
#     ws.run_forever()  

# if __name__ == "__main__":
#     websocket_data()


    #     # if time_frame == 's':
    #     #     timedelta = pd.Timedelta(seconds=kline_time)
    #     if time_frame == 'm':
    #         timedelta = pd.Timedelta(minutes=kline_time)
    #         print(timedelta)
    #     # elif time_frame == 'h':
    #     #     timedelta = pd.Timedelta(hours=kline_time)
    #     # elif time_frame == 'd':
    #     #     timedelta = pd.Timedelta(days=kline_time)
    #     # elif time_frame == 'w':
    #     #     timedelta = pd.Timedelta(weeks=kline_time)
    #     # elif time_frame == 'M':
    #     #     timedelta = pd.Timedelta(days=int(kline_time*30))



    # @log_exceptions_decorator
    # async def refactor_klines_data_func(self, kline_websocket_data, first_klines_data, is_pop, kline_time, time_frame):
    #     is_pop = True
    #     last_time = first_klines_data.index[-1]
    #     if time_frame == 'm':
    #         timedelta = pd.Timedelta(minutes=kline_time)
    #     new_time = last_time + timedelta if is_pop else last_time
        
    #     if is_pop:
    #         first_klines_data = first_klines_data.iloc[1:]  # Удаляем первую строку
    #         new_row = pd.Series({
    #             'Time': new_time,
    #             'Open': float(kline_websocket_data['o']),
    #             'High': float(kline_websocket_data['h']),
    #             'Low': float(kline_websocket_data['l']),
    #             'Close': float(kline_websocket_data['c']),
    #             'Volume': float(kline_websocket_data['v'])
    #         })
    #         first_klines_data = first_klines_data.append(new_row, ignore_index=False)  
    #     else:
    #         first_klines_data.loc[last_time, 'Open'] = float(kline_websocket_data['o'])
    #         first_klines_data.loc[last_time, 'High'] = float(kline_websocket_data['h'])
    #         first_klines_data.loc[last_time, 'Low'] = float(kline_websocket_data['l'])
    #         first_klines_data.loc[last_time, 'Close'] = float(kline_websocket_data['c'])
    #         first_klines_data.loc[last_time, 'Volume'] = float(kline_websocket_data['v'])

    #     return first_klines_data


    # async def refactor_klines_data_func(self, kline_websocket_data, first_klines_data, is_pop, kline_time, time_frame):
    #     last_time = first_klines_data.index[-1]
    #     print(last_time)
    #     if time_frame == 'm':
    #         timedelta = pd.Timedelta(minutes=kline_time)
    #         print(timedelta)
    #     new_time = last_time + timedelta if is_pop else last_time
    #     new_row = pd.Series({
    #         'Time': new_time,
    #         'Open': float(kline_websocket_data['o']),
    #         'High': float(kline_websocket_data['h']),
    #         'Low': float(kline_websocket_data['l']),
    #         'Close': float(kline_websocket_data['c']),
    #         'Volume': float(kline_websocket_data['v'])
    #     })
    #     if is_pop:
    #         first_klines_data = first_klines_data.iloc[1:]            
    #     new_df = pd.DataFrame([new_row])  # Создаем DataFrame из новой строки
    #     new_df = new_df.set_index('Time')  # Устанавливаем индекс 'Time' для нового DataFrame
    #     first_klines_data = pd.concat([first_klines_data, new_df])  # Объединяем новый DataFrame с первоначальным
    #     return first_klines_data



    # @log_exceptions_decorator
    # async def get_processing_signal(self):
    #     trade_sign = None
    #     left_time_to_round = self.time_calibrator(self.kline_time, self.time_frame)
    #     # print(left_time_to_round)
    #     time.sleep(left_time_to_round)
    #     # print(int(time.time()*1000))
    #     # self.first_klines_data = self.get_klines(self.symbol)      
    #     return self.get_signals(self.get_klines(self.symbol), self.ema1_period, self.ema2_period)
    #     # length_of_dataframe = self.first_klines_data.shape[0]
    #     # print("Длина первого датафрейма:", length_of_dataframe)
    #     # print(self.first_klines_data)
    #     # return trade_sign

   
    # @log_exceptions_decorator
    # def time_calibrator(self, kline_time, time_frame):
    #     wait_time = 0 
    #     if time_frame == 'm':
    #         wait_time = ((60*kline_time) - (time.time()%60) + 1)
    #     elif time_frame == 'h':
    #         wait_time = ((3600*kline_time) - (time.time()%3600) + 1)
    #     elif time_frame == 'd':
    #         wait_time = ((86400*kline_time) - (time.time()%86400) + 1)

    #     return int(wait_time)


    # @log_exceptions_decorator
    # def make_order(self, symbol, qty, defender, is_closing, market_type='MARKET'): 
    #     params = {}        
    #     url = self.URL_PATTERN_DICT['create_order_url']       
    #     params["symbol"] = symbol        
    #     params["type"] = market_type
    #     params["quantity"] = qty
      
    #     # if market_type == 'LIMIT':            
    #     #     params["price"] = target_price
    #     #     params["timeinForce"] = 'GTC' 
            
    #     # if market_type == 'STOP_MARKET':
    #     #     params['stopPrice'] = target_price
    #     #     params['closePosition'] = True 
  
    #     if defender == 1*is_closing:
    #         side = 'BUY'
    #     elif defender == -1*is_closing:
    #         side = "SELL" 
    #     params["side"] = side
    #     params = self.get_signature(params)
    #     return self.HTTP_request(url, method='POST', headers=self.header, params=params)



    
    # @log_exceptions_decorator
    # def time_calibrator(self, kline_time, time_frame):
    #     wait_time = 0 
    #     if time_frame == 'm':
    #         wait_time = ((60*kline_time) - (time.time()%60) + 1)
    #     elif time_frame == 'h':
    #         wait_time = ((3600*kline_time) - (time.time()%3600) + 1)
    #     elif time_frame == 'd':
    #         wait_time = ((86400*kline_time) - (time.time()%86400) + 1)

    #     return int(wait_time)
 
    # @log_exceptions_decorator
    # def time_calibrator(self, kline_time, time_frame):
    #     wait_time = 0 
    #     current_time_ms = int(time.time() * 1000)
    #     # ////////////////////////////////////////////
    #     if time_frame == 'm':
    #         wait_time = ((60 * kline_time * 1000) - (current_time_ms % (60 * 1000)) + 1000)
    #     elif time_frame == 'h':
    #         wait_time = ((3600 * kline_time * 1000) - (current_time_ms % (3600 * 1000)) + 1000)
    #     elif time_frame == 'd':
    #         wait_time = ((86400 * kline_time * 1000) - (current_time_ms % (86400 * 1000)) + 1000)
    #     # ////////////////////////////////////////////
    #     return int(wait_time)



# import asyncio
# import aiohttp
# import random
# import json

# async def websocket_handler():
#     url = 'wss://stream.binance.com:9443/stream?streams=' 
#     coins_in_squeezeOn_arg = ['BTCUSDT'] 

#     while True:
#         print('hello')
#         ws = None   
#         streams = [f"{symbol.lower()}@kline_1s" for symbol in coins_in_squeezeOn_arg]

#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.ws_connect(url) as ws:
#                     subscribe_request = {
#                         "method": "SUBSCRIBE",
#                         "params": streams,
#                         "id": random.randrange(11,111111)
#                     }

#                     try:
#                         await ws.send_json(subscribe_request)
#                     except Exception as ex:
#                         print(ex)
#                     async for msg in ws:
#                         if ws.closed:
#                             print(f"ws.closed: {ws.closed}")
#                             return 
                                        
#                         if msg.type == aiohttp.WSMsgType.TEXT:
#                             try:
#                                 data = json.loads(msg.data)                                        
#                                 symbol = data.get('data',{}).get('s')  
#                                 print(symbol)                                 
#                                 last_close_price = float(data.get('data',{}).get('k',{}).get('c')) 
#                                 print(last_close_price) 
#                             except Exception as ex:
#                                 print(ex)
#                                 continue
#         except Exception as ex:
#             print(ex)

# if __name__=="__main__":
#     asyncio.run(websocket_handler())


# import asyncio
# import aiohttp
# import random
# import json

# async def websocket_handler():
#     url = 'wss://stream.binance.com:9443/ws/'
#     symbol = 'btcusdt'

#     while True:
#         print('hello')
#         ws = None   

#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.ws_connect(url + f"{symbol}@kline_1s") as ws:
#                     subscribe_request = {
#                         "method": "SUBSCRIBE",
#                         "params": [f"{symbol.lower()}@kline_1s"],
#                         "id": random.randrange(11,111111)
#                     }

#                     try:
#                         await ws.send_json(subscribe_request)
#                     except Exception as ex:
#                         pass
#                         # print(ex)
#                     async for msg in ws:
#                         if ws.closed:
#                             print(f"ws.closed: {ws.closed}")
#                             return 
                                    
#                         if msg.type == aiohttp.WSMsgType.TEXT:
#                             try:
#                                 data = json.loads(msg.data)
#                                 # print(data)
#                                 kline_data = data.get('k', {})
#                                 if kline_data:
#                                     last_close_price = float(kline_data.get('c'))
#                                     print(last_close_price)
#                                 # else:
#                                 #     print("No kline data available")
#                             except Exception as ex:
#                                 # print(ex)
#                                 continue

#         except Exception as ex:
#             pass

# if __name__=="__main__":
#     asyncio.run(websocket_handler())




    # def calculate_stop_loss_ratio(self, direction, enter_price, candles_df, stop_loss_type):
    #     stop_loss_ratio = None
    #     period = self.first_klines_data.shape[0]
    #     if direction == 1:        
    #         if stop_loss_type == 'LAST_MIN':
    #             lows = candles_df['Low']
    #             local_minima = lows.rolling(window=period, min_periods=period).min()
    #             last_local_minima = local_minima[local_minima.index < enter_price].iloc[-1]
    #             stop_loss_ratio = (enter_price - last_local_minima) / enter_price
    #         elif stop_loss_type == 'ABSOLUTE_MIN':
    #             absolute_min = candles_df['Low'].min()
    #             stop_loss_ratio = (enter_price - absolute_min) / enter_price
    #     elif direction == -1:
    #         if stop_loss_type == 'LAST_MIN':
    #             highs = candles_df['High']
    #             local_maxima = highs.rolling(window=period, min_periods=period).max()
    #             last_local_maxima = local_maxima[local_maxima.index > enter_price].iloc[-1]
    #             stop_loss_ratio = abs(enter_price - last_local_maxima) / enter_price
    #         elif stop_loss_type == 'ABSOLUTE_MIN':
    #             absolute_max = candles_df['High'].max()
    #             stop_loss_ratio = abs(enter_price - absolute_max) / enter_price
        
    #     return stop_loss_ratio

    
    # @log_exceptions_decorator
    # def calculate_stop_loss_ratio(self, direction, enter_price, candles_df):
    #     stop_loss_ratio = None
    #     period = self.first_klines_data.shape[0]
    #     if direction == 1:        
    #         lows = candles_df['Low']
    #         local_minima = lows.rolling(window=period, min_periods=period).min()
    #         last_local_minima = local_minima[local_minima.index < enter_price].iloc[-1]
    #         stop_loss_ratio = (enter_price - last_local_minima) / enter_price
    #     elif direction == -1:
    #         highs = candles_df['High']
    #         local_maxima = highs.rolling(window=period, min_periods=period).max()
    #         last_local_maxima = local_maxima[local_maxima.index > enter_price].iloc[-1]
    #         stop_loss_ratio = abs(enter_price - last_local_maxima) / enter_price
        
    #     return stop_loss_ratio

# tralling_stop_loss_engin_response = None


        # print(symbol_data)
        # tick_size = float(symbol_data['filters'][0]["tickSize"])         
        # tick_size = str(float(tick_size))
        # quantity_precision1 = Decimal(tick_size).normalize().to_eng_string()        
        # quantity_precision1 = len(quantity_precision1.split('.')[1]) 
        # print(f"quantity_precision1: {quantity_precision1}")


            # if order_answer['status'] == 'NEW':
            #     create_order_success_flag = True
            #     if is_closing == 1:
            #         print(f'The {side} position was opened successfully!')
            #     else:
            #         print(f'The current position was closed successfully!')



            # else:
            #     print("Some problems with getting get_signal_val")



# print(round(0.003445563434, 7))

# import time 
# import random
# from random import choice

# def psevdo_tralling_stop_loss_monitoring():
#     stop_loss_multiplier = -1
#     trigger_multiplier = 1
#     price = 63010
#     entry_price = 63000
#     stop_loss_ratio = 0.01
#     direction = 1 # LONG POSITION
#     stop_loss = entry_price * (1 + direction*stop_loss_ratio * stop_loss_multiplier)
#     trigger_price = entry_price * (1 + direction*stop_loss_ratio * trigger_multiplier)
#     random_list = [1,1,2,2,2,2,2,2]

#     while True:
#         # random_for_math_sign = random.randrange(0,10)
#         random_for_math_sign = choice(random_list)
#         math_sign = '+' if random_for_math_sign% 2 == 0 else '-' 
#         random_val = random.randrange(200, 500)
#         price = eval(f"{price}{math_sign}{random_val}")
#         jump_trigger_price_condition = price >= trigger_price if direction == 1 else price <= trigger_price
#         if direction == 1:
#             if jump_trigger_price_condition:    
#                 stop_loss_multiplier += 1
#                 trigger_multiplier += 1
#                 stop_loss = entry_price * (1 + direction*stop_loss_ratio * stop_loss_multiplier)
#                 trigger_price = entry_price * (1 + direction*stop_loss_ratio * trigger_multiplier)
#                 print(f"stop_loss: {stop_loss}")
#             elif price <= stop_loss:
#                 # sell_position(price)
#                 if stop_loss_multiplier == -1:
#                     print(f"stop_loss_multiplier: {stop_loss_multiplier}")
#                     print("Position closed with a loss/Позиция закрыта c убытком")
#                 elif stop_loss_multiplier == 0:
#                     print(f"stop_loss_multiplier: {stop_loss_multiplier}")
#                     print("The position is closed at the breakeven point/Позиция закрыта в точке безубыточности")
#                 else:
#                     print(f"stop_loss_multiplier: {stop_loss_multiplier}")
#                     print("position closed with a profit/Позиция закрыта c прибылью")
#                 return ('Func was returned!')
#         time.sleep(1)

# if __name__=="__main__":
#     psevdo_tralling_stop_loss_monitoring()

# import decimal


# real_buy_price = 0.0000000000000000000000000000000001
# real_buy_price = 1e-34 + 10
# real_buy_price = decimal.Decimal(str(real_buy_price))
# real_buy_price = format(real_buy_price, 'f')
# print(real_buy_price)

# ema_list = [5, 10, None]
# print(ema_list[2])



# user_agents = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
# ]


# class COIN_MARKET_PARSER():
#     def __init__(self) -> None:
#         # super().__init__()
#         pass

#     def coin_market_cup_engin(self, url, headers):            
#         data_tickers = []
#         coin_name = None
#         r = requests.get(url, headers=headers)
#         soup = BeautifulSoup(r.text, 'lxml')
#         tablee = soup.find('tbody').find_all('tr', recursive=False)

#         for tik in tablee:
#             coin_name = None
#             coin_name_pre = None
#             try:                
#                 coin_name_pre = tik.find_all('td')[2]            
#                 if coin_name_pre:                   
#                     try:
#                         coin_name = coin_name_pre.find_all('p')[-1].text.strip()
#                         if coin_name.upper() != 'USDT':
#                             data_tickers.append(coin_name+'USDT')    
#                     except:                      
#                         # print(coin_name_pre)
#                         coin_name = coin_name_pre.find('span', class_="crypto-symbol").text.strip()
#                         if coin_name.upper() != 'USDT':
#                             data_tickers.append(coin_name+'USDT') 

#             except Exception as ex:
#                 print(ex)                

#         return data_tickers

#     def coin_market_cup_parser(self):
#         tickers = None
#         tickers_list = []
#         headers = {
#             'Authority': 'coinmarketcap.com',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#             # 'accept-language': 'en-US,en;q=0.9',
#             # 'cache-control': 'max-age=0',
#             # 'if-none-match': '"10w167pxbou88xt"',
#             # 'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
#             # 'sec-ch-ua-mobile': '?0',
#             # 'sec-ch-ua-platform': '"Linux"',
#             # 'sec-fetch-dest': 'document',
#             # 'sec-fetch-mode': 'navigate',
#             # 'sec-fetch-site': 'none',
#             # 'sec-fetch-user': '?1',
#             # 'upgrade-insecure-requests': '1',
#             'User-Agent': choice(user_agents)
           
#         }
#         url = f'https://coinmarketcap.com/ru/'
#         return self.coin_market_cup_engin(url, headers)


            # if create_order_success_flag:
            #     create_order_success_flag = False                    
            #     print(self.response_trading_list)
            #     # //////////////////////////////////////////////////////////////////
            #     self.enter_price, self.executed_qty = self.post_trading_info_template(self.response_trading_list, self.qty, self.cur_price)                     
            #     # /////////////////////////////////////////////////////////////////////
            #     stop_loss_ratio = self.calculate_stop_loss_ratio(self.direction, self.enter_price, self.cur_klines_data, self.stop_loss_type, self.default_stop_loss_ratio_val)  
            #     print(f"stop_loss_ratio: {stop_loss_ratio}") 
            #     # устанавливаем фиксированный стоп лосс ордер в качестве подстраховки:
            #     target_price = self.enter_price* (1 - self.direction*stop_loss_ratio)
            #     self.direction = self.direction*(-1)
            #     self.response_trading_list, create_order_success_flag = self.make_orders_template(self.qty, 'STOP_MARKET', target_price)             
            #     response_trading_total_list += self.response_trading_list
            #     self.direction = self.direction*(-1)
            #     if self.stop_loss_global_type == 'TRAILLING_GLOBAL_TYPE':
            #         # self.tralling_stop_order(self.symbol, self.executed_qty, side, stop_loss_ratio)
            #         # self.stop_order_total_multipliter = await self.stop_logic_price_monitoring(self.symbol, self.direction, self.enter_price, stop_loss_ratio) # old 
            #         stop_loss_ratio = None
            #         # self.stop_order_total_multipliter = 0 # test
            #         print(f"stop_order_total_multipliter: {self.stop_order_total_multipliter}")
            #         if self.stop_order_total_multipliter is not None:                            
            #             if not self.is_open_position_true(self.symbol):                        
            #                 print("The current position probably was closed manualy or as result some others anomaly...")
            #                 self.default_post_trading_vars()
            #                 # return # test
            #                 continue
            #             print("Position is avialable yet")
            #             self.is_closing = -1
            #             self.response_trading_list, self.close_position_success_flag = self.make_orders_template(self.executed_qty)
            #             response_trading_total_list += self.response_trading_list
            #             if self.close_position_success_flag:
            #                 show_post_trade_info_answer = self.show_post_trade_info(self.stop_order_total_multipliter)   
            #                 print(show_post_trade_info_answer)                             
            #                 self.default_post_trading_vars()                         
            #             else:
            #                 print('Some problems with closing position...')                            
            #         else:
            #             print("Stop_logic_price_monitoring func was finished uncorrectly...")



    # def response_order_logger(self, order_answer, side, market_type):
    #     create_order_success_flag = False        
    #     if order_answer['status'] == 'FILLED':
    #         create_order_success_flag = True
    #         if is_closing == 1:
    #             print(f'The {side} position {market_type} type order was opened successfully!')
    #         else:
    #             print(f'The current position was closed successfully!')
    #     elif order_answer['status'] == 'PARTIALLY_FILLED':
    #         create_order_success_flag = True
    #         if is_closing == 1:
    #             print(f'The {side} position {market_type} type order was opened successfully!')
    #         else:
    #             print(f'The current position was closed partially!') 
    #     else:
    #         print(f'The {side} position was NOT opened...')
    #     return create_order_success_flag

    # def response_order_logger(self, order_answer, side, market_type):   
    #     if order_answer['status'] == 'FILLED':
    #         print(f'The {side} position {market_type} type order was opened successfully!')
    #         return True
    #     elif order_answer['status'] == 'PARTIALLY_FILLED':
    #         print(f'The {side} position {market_type} type order was opened with a status PARTIALLY_FILLED')
    #         return True
    #     print(f'The {side} position {market_type} type orde was NOT opened...')
    #     return False

    # def usdt_to_qnt_converter(self, symbol, depo, symbol_info, cur_price):
    #     qty = None
    #     symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)
    #     print(symbol_data)
    #     # //////////////////////
    #     quantity_precision = int(float(symbol_data['quantityPrecision']))
    #     price_precision = int(symbol_data['pricePrecision']) 
    #     print(f"quantity_precision: {quantity_precision}")
    #     qty = round(depo / cur_price, quantity_precision)
    #     # min_qnt = float(symbol_data['filters'][1]['minQty'])
    #     # print(f"min_qnt: {min_qnt}")
    #     # max_qnt = float(symbol_data['filters'][1]['maxQty']) 
    #     # if qty <= min_qnt:
    #     #     return min_qnt, quantity_precision              
    #     # elif qty >= max_qnt:
    #     #     return max_qnt, quantity_precision    
    #     return qty, price_precision

# {'symbol': 'DOGEUSDT', 'pair': 'DOGEUSDT', 'contractType': 'PERPETUAL', 'deliveryDate': 4133404800000, 'onboardDate': 1569398400000, 'status': 'TRADING', 'maintMarginPercent': '2.5000', 'requiredMarginPercent': '5.0000', 'baseAsset': 'DOGE', 'quoteAsset': 'USDT', 'marginAsset': 'USDT', 'pricePrecision': 6, 'quantityPrecision': 0, 'baseAssetPrecision': 8, 'quotePrecision': 8, 'underlyingType': 'COIN', 'underlyingSubType': ['Meme'], 'settlePlan': 0, 'triggerProtect': '0.1000', 'liquidationFee': '0.010000', 'marketTakeBound': '0.10', 'maxMoveOrderLimit': 10000, 'filters': [{'maxPrice': '30', 'minPrice': '0.002440', 'filterType': 'PRICE_FILTER', 'tickSize': '0.000010'}, {'minQty': '1', 'maxQty': '50000000', 'stepSize': '1', 'filterType': 'LOT_SIZE'}, {'filterType': 'MARKET_LOT_SIZE', 'minQty': '1', 'maxQty': '30000000', 'stepSize': '1'}, {'limit': 200, 'filterType': 'MAX_NUM_ORDERS'}, {'filterType': 'MAX_NUM_ALGO_ORDERS', 'limit': 10}, {'filterType': 'MIN_NOTIONAL', 'notional': '5'}, {'filterType': 'PERCENT_PRICE', 'multiplierUp': '1.1000', 'multiplierDecimal': '4', 'multiplierDown': '0.9000'}], 'orderTypes': ['LIMIT', 'MARKET', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET'], 'timeInForce': ['GTC', 'IOC', 'FOK', 'GTX', 'GTD']}