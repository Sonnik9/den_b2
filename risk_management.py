# import time
# import random
# import asyncio
# import aiohttp
# import json
from datetime import datetime, timedelta
from techniques import STRATEGY
from api_binance import BINANCE_API
from log import log_exceptions_decorator

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
    
class STATISTIC(BINANCE_API):
    def __init__(self):  
        super().__init__()  
    
    def last_statistic(self, symbol):        
        init_order_price, oposit_order_price = 0, 0
        try:
            orders = self.get_all_orders(symbol)
            orders= sorted(orders, key=lambda x: x["time"], reverse=True)
            the_orders = []
            for order in orders:
                if len(the_orders) == 2:
                    break
                try:
                    if order["status"] == 'FILLED':                        
                        the_orders = [order] + the_orders                        
                except:
                    pass
            init_order_price = float(the_orders[0].get('avgPrice', None))
            oposit_order_price = float(the_orders[1].get('avgPrice', None))
            if the_orders[0].get('side', None) == the_orders[1].get('side', None):
                return 0, 0, 0, self.depo
            if the_orders[0].get('side', None) == 'BUY':
                if init_order_price - oposit_order_price > 0:
                    return -1, init_order_price, oposit_order_price, self.depo
                elif init_order_price - oposit_order_price < 0:
                    return 1, init_order_price, oposit_order_price, self.depo
            elif the_orders[0].get('side', None) == 'SELL':
                if init_order_price - oposit_order_price > 0:
                    return 1, init_order_price, oposit_order_price, self.depo
                elif init_order_price - oposit_order_price < 0:
                    return -1, init_order_price, oposit_order_price, self.depo
        except Exception as ex:
            print(ex)
        return 0, init_order_price, oposit_order_price, self.depo
    # /////////////////////////////////////////////////////////////
    def get_next_show_statistic_time(self):
        current_time = datetime.now()
        target_time = current_time.replace(hour=self.show_statistic_hour, minute=0, second=0)
        if current_time >= target_time:            
            target_time += timedelta(days=1)        
        return target_time
    
    def show_statistic_signal(self, target_time): 
        now_time = datetime.now()      
        if now_time >= target_time:
            target_time = self.get_next_show_statistic_time()             
            return True, target_time          
        return False, target_time
    # /////////////////////////////////////////////////////////////
    def statistic_calculations(self, daily_trade_history_list):
        result_statistic_dict = {}
        if not isinstance(daily_trade_history_list, list) or len(daily_trade_history_list) == 0:
            return {}
        try:
            result_statistic_dict["win_count"] = win_count = sum(1 for win_los, _, _, _ in daily_trade_history_list if win_los == 1)
            result_statistic_dict["loss_count"] = loss_count = sum(1 for win_los, _, _, _ in daily_trade_history_list if win_los == -1)
        except Exception as ex:
            print(ex)
        try:
            total_trade_count = win_count + loss_count
            if total_trade_count != 0:
                result_statistic_dict["win_per"] = win_per = (win_count*100)/total_trade_count
                result_statistic_dict["loss_per"] = loss_per = (loss_count*100)/total_trade_count
                if loss_count != 0 and win_count != 0:
                    result_statistic_dict["win_to_loss_relation"] = win_to_loss_relation = win_count/ loss_count
                else:
                    result_statistic_dict["win_to_loss_relation"] = win_to_loss_relation = f"{win_count}/{loss_count}"
                result_statistic_dict["win_to_loss_statistik"] = win_to_loss_statistik = f"{win_count}:{loss_count}"
        except Exception as ex:
            print(ex)
        
        try:
            result_statistic_dict["max_profit_abs"] = max_profit_abs = max((abs(init_order_price - oposit_order_price)/init_order_price)* last_depo for win_los, init_order_price, oposit_order_price, last_depo in daily_trade_history_list if win_los == 1)
            result_statistic_dict["max_drawdown_abs"] = max_drawdown_abs = min(-1*(abs(init_order_price - oposit_order_price)/init_order_price)* last_depo for win_los, init_order_price, oposit_order_price, last_depo in daily_trade_history_list if win_los == -1)
            result_statistic_dict["total_profit_abs"] = total_profit_abs = sum((abs(init_order_price - oposit_order_price)/init_order_price)* last_depo for win_los, init_order_price, oposit_order_price, last_depo in daily_trade_history_list if win_los == 1)
            result_statistic_dict["total_losses_abs"] = total_losses_abs = sum(-1*(abs(init_order_price - oposit_order_price)/init_order_price)* last_depo for win_los, init_order_price, oposit_order_price, last_depo in daily_trade_history_list if win_los == -1)
        except Exception as ex:
            print(ex)

        return result_statistic_dict