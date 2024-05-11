# import time 
# import random
# import asyncio
# import aiohttp
# import json
from log import log_exceptions_decorator
from techniques import STRATEGY

class STOP_LOGIC(STRATEGY):
    def __init__(self):  
        super().__init__()  

    @log_exceptions_decorator
    def calculate_stop_loss_ratio(self, direction, enter_price, candles_df, stop_loss_type, fixed_stop_loss_ratio_val):
        # /////////////////////////////////////////////////////
        if enter_price == 0:
            return
        stop_loss_ratio = None
        atr_period = period = int(candles_df.shape[0]/ 2.5) + 1  
        # atr_period = 12 if atr_period < 12 else atr_period
        # print(f"period : {period}")
        if stop_loss_type == 'FIXED':
            return fixed_stop_loss_ratio_val
        if stop_loss_type == 'ATR_VAL':
            _, atr_value  = self.calculate_atr(candles_df, atr_period)
            stop_loss_ratio = round(atr_value / enter_price * 1.618, 7)                

        if direction == 1:
            if stop_loss_type == 'LAST_MIN':
                lows = candles_df['Low']
                local_minima = lows.rolling(window=period, min_periods=period).min()
                last_local_minima = local_minima[local_minima.index < candles_df.index[-1]].iloc[-1]
                if last_local_minima >= enter_price:
                    return fixed_stop_loss_ratio_val
                else:
                    stop_loss_ratio = (enter_price - last_local_minima) / enter_price
            elif stop_loss_type == 'ABSOLUTE_MIN':
                absolute_min = candles_df['Low'].min()
                if absolute_min >= enter_price:
                    return fixed_stop_loss_ratio_val
                else:
                    stop_loss_ratio = (enter_price - absolute_min) / enter_price
        elif direction == -1:
            if stop_loss_type == 'LAST_MIN':
                highs = candles_df['High']
                local_maxima = highs.rolling(window=period, min_periods=period).max()
                last_local_maxima = local_maxima[local_maxima.index > candles_df.index[0]].iloc[-1]
                if last_local_maxima <= enter_price:
                    return fixed_stop_loss_ratio_val
                else:
                    stop_loss_ratio = abs(enter_price - last_local_maxima) / enter_price
            elif stop_loss_type == 'ABSOLUTE_MIN':
                absolute_max = candles_df['High'].max()
                if absolute_max <= enter_price:
                    return fixed_stop_loss_ratio_val
                else:
                    stop_loss_ratio = abs(enter_price - absolute_max) / enter_price

        if stop_loss_ratio is not None and stop_loss_ratio < 0.0015:
            print(f"stop_loss_ratio < 0.0015: {stop_loss_ratio < 0.0015}")
            return fixed_stop_loss_ratio_val
        return round(stop_loss_ratio, 7)
    
    # @log_exceptions_decorator
    # def tralling_stop_loss_engin(self, price, enter_price, direction, stop_loss_ratio, stop_loss_multiplier, stop_loss, trigger_price, trigger_multiplier): 
    #     # print(price, enter_price, direction, stop_loss_ratio, stop_loss_multiplier, stop_loss, trigger_price, trigger_multiplier)
    #     jump_trigger_price_condition = False
    #     stop_loss_trigger = False
    #     jump_trigger_price_condition = price >= trigger_price if direction == 1 else price <= trigger_price
    #     stop_loss_trigger = price <= stop_loss if direction == 1 else price >= stop_loss

    #     if jump_trigger_price_condition:    
    #         stop_loss_multiplier += 1
    #         trigger_multiplier += 1
    #         stop_loss = enter_price * (1 + direction*stop_loss_ratio * stop_loss_multiplier)
    #         trigger_price = enter_price * (1 + direction*stop_loss_ratio * trigger_multiplier)
    #         print(f"Stop_loss is moved on: {stop_loss}")
    #     elif stop_loss_trigger:
    #         print(f"stop_loss_trigger == True")
    #         return -1, stop_loss_multiplier, stop_loss, trigger_price, trigger_multiplier

    #     return 1, stop_loss_multiplier, stop_loss, trigger_price, trigger_multiplier
        
    # @log_exceptions_decorator
    # async def stop_logic_price_monitoring(self, symbol, direction, enter_price, stop_loss_ratio):
    #     # /////////////////////////////////////
    #     last_close_price = None      
    #     url = 'wss://stream.binance.com:9443/ws/'
    #     # /////////////////////////////////////
    #     max_retries = 10
    #     retry_delay = 1  # seconds
    #     retries = 0
    #     # /////////////////////////////////////
    #     is_closing = 1
    #     stop_loss_multiplier = -1
    #     trigger_multiplier = 1
    #     stop_loss = enter_price * (1 + direction*stop_loss_ratio * stop_loss_multiplier)
    #     trigger_price = enter_price * (1 + direction*stop_loss_ratio * trigger_multiplier)
    #     # /////////////////////////////////////
    #     while retries < max_retries:            
    #         try:
    #             async with aiohttp.ClientSession() as session:
    #                 async with session.ws_connect(url + f"{symbol}@kline_1s") as ws:
    #                     subscribe_request = {
    #                         "method": "SUBSCRIBE",
    #                         "params": [f"{symbol.lower()}@kline_1s"],
    #                         "id": random.randrange(11,111111)
    #                     }
    #                     print('Stop_logic_price_monitoring start processing!')                        
    #                     try:
    #                         await ws.send_json(subscribe_request)
    #                     except:
    #                         pass

    #                     async for msg in ws:
    #                         if msg.type == aiohttp.WSMsgType.TEXT:
    #                             try:
    #                                 data = json.loads(msg.data)
    #                                 kline_websocket_data = data.get('k', {})
    #                                 if kline_websocket_data:
    #                                     # print(kline_websocket_data)
    #                                     last_close_price = float(kline_websocket_data.get('c'))
    #                                     # print(f"last_close_price: {last_close_price}")
    #                                     # await asyncio.sleep(2)
    #                                     try:
    #                                         is_closing, stop_loss_multiplier, stop_loss, trigger_price, trigger_multiplier = self.tralling_stop_loss_engin(last_close_price, enter_price, direction, stop_loss_ratio, stop_loss_multiplier, stop_loss, trigger_price, trigger_multiplier)                                            
    #                                         if is_closing == -1:                                                                      
    #                                             print(is_closing, stop_loss_multiplier, stop_loss, trigger_price, trigger_multiplier)
    #                                             return stop_loss_multiplier
    #                                     except Exception as ex:
    #                                         print(ex)
                                        
    #                             except Exception as ex:
    #                                 continue

    #         except Exception as ex:
    #             print(f"An error occurred: {ex}")
    #             retries += 1
    #             await asyncio.sleep(retry_delay * (2 ** retries))  # Exponential backoff
    #     return