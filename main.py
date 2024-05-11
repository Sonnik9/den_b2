import telebot
from telebot import types 
import time 
# import decimal
import math
# import random
import asyncio
# import aiohttp
# import json
from api_binance import BINANCE_API
from utils import UTILS, COIN_MARKET_API_PARSER
from risk_management import STOP_LOGIC
from log import total_log_instance, log_exceptions_decorator

class CONNECTOR_TG(BINANCE_API, UTILS, COIN_MARKET_API_PARSER, STOP_LOGIC):
    def __init__(self):  
        super().__init__()  
        self.bot = telebot.TeleBot(self.tg_api_token)
        self.menu_markup = self.create_menu() 
        self.last_message = None

    def create_menu(self):
        menu_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        button1 = types.KeyboardButton("START")
        button2 = types.KeyboardButton("STOP")    
        menu_markup.add(button1, button2)        
        return menu_markup

class TG_ASSISTENT(CONNECTOR_TG):
    def __init__(self):
        super().__init__()

    def connector_func(self, message, response_message):
        retry_number = 3
        decimal = 1.1       
        for i in range(retry_number):
            try:
                self.bot.send_message(message.chat.id, response_message)                
                return message.text
            except Exception as ex:
                print(ex)

                time.sleep(1.1 + i*decimal)                   
        return None
    
class TEMPLATES(TG_ASSISTENT):
    def __init__(self):  
        super().__init__()

    @log_exceptions_decorator
    def make_orders_template(self, qty, market_type, target_price):
        # //////////////////////////////////////////////
        create_order_success_flag = False
        response_list = []
        self.direction = self.direction*self.is_closing
        side = 'BUY' if self.direction == 1 else 'SELL'
        try:
            order_answer = self.make_order(self.symbol, qty, side, market_type, target_price)
            # print(order_answer)
            response_list.append(order_answer)
            if order_answer['status'] == 'FILLED':
                create_order_success_flag = True
                if self.is_closing == 1:
                    print(f'The {side} position {market_type} type order was opened successfully!')
                else:
                    print(f'The current position was closed successfully!')
            elif order_answer['status'] == 'PARTIALLY_FILLED':
                create_order_success_flag = True
                if self.is_closing == 1:
                    print(f'The {side} position {market_type} type order was opened successfully!')
                else:
                    print(f'The current position was closed partially!') 
            else:
                print(f'The {side} position was NOT opened...')

        except Exception as ex:
            print(ex)

        return response_list, create_order_success_flag
    
    def pre_trading_info_template(self):
        symbol_info = self.get_excangeInfo()  
        cur_price = self.cur_klines_data['Close'].iloc[-1]
        qty, _ = self.usdt_to_qnt_converter(self.symbol, self.depo, symbol_info, cur_price)
        print("qty, cur_price:")
        self.from_anomal_view_to_normal([qty, cur_price]) 
        return cur_price, qty    
    
    def post_trading_info_template(self, response_trading_list, qty, cur_price):
        # //////////////////////////////////////////////////////////////////
        executed_qty = float(response_trading_list[0].get('executedQty', qty))
        enter_price = float(response_trading_list[0].get('avgPrice', cur_price)) 
        order_id = response_trading_list[0].get('orderId', None)
        print("qty, enter_price:")
        self.from_anomal_view_to_normal([executed_qty, enter_price])  
        return enter_price, executed_qty 
        
    def get_top_coins_template(self):
        def go_filter(all_binance_tickers, coinsMarket_tickers):
            top_pairs = []
            
            exclusion_contains_list = ['UP', 'DOWN', 'RUB', 'EUR']

            if all_binance_tickers:
                if not self.price_filter_flag:
                    self.MIN_FILTER_PRICE = 0
                    self.MAX_FILTER_PRICE = math.inf                   

                top_pairs = [ticker for ticker in all_binance_tickers if
                                ticker['symbol'].upper().endswith('USDT') and
                                not any(exclusion in ticker['symbol'].upper() for exclusion in exclusion_contains_list) and
                                (float(ticker['lastPrice']) >= self.MIN_FILTER_PRICE) and (
                                        float(ticker['lastPrice']) <= self.MAX_FILTER_PRICE)]

                # print(top_pairs[:4])
                top_pairs = sorted(top_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
                top_pairs = top_pairs[:self.SLICE_VOLUME_BINANCE_PAIRS]
                # print(top_pairs)

                if self.min_volume_usdtFilter_flag:
                    top_pairs = [x for x in top_pairs if float(x['quoteVolume']) >= self.MIN_VOLUM_USDT]

                if self.slice_volatilyty_flag:
                    top_pairs = sorted(top_pairs, key=lambda x: abs(float(x['priceChangePercent'])), reverse=True)
                    top_pairs = top_pairs[:self.SLICE_VOLATILITY]
                    # print(top_pairs)
                if self.daily_filter_direction == 1:
                    top_pairs = [x for x in top_pairs if float(x['priceChange']) > 0]
                elif self.daily_filter_direction == -1:
                    top_pairs = [x for x in top_pairs if float(x['priceChange']) < 0]

                return [x['symbol'] for x in top_pairs if x['symbol'] not in self.problem_pairs and x['symbol'] in coinsMarket_tickers]
                # return [x['symbol'] for x in top_pairs if x['symbol'] not in self.problem_pairs]
        all_binance_tickers = self.get_all_tickers()
        coinsMarket_tickers = self.coin_market_cup_top(self.coinMarketCup_api_token, self.TOP_MARKET_CUP) 
        return go_filter(all_binance_tickers, coinsMarket_tickers)        

class MAIN_CONTROLLER(TEMPLATES):
    def __init__(self):  
        super().__init__() 

    @log_exceptions_decorator
    async def get_signal_shell(self): 
        self.cur_klines_data = self.get_klines(self.symbol)
        return self.get_signals(self.strategy_name, self.smoothing_crossover_condition, self.cur_klines_data, self.ema1_period, self.ema2_period)
  
    @log_exceptions_decorator
    async def main_func(self):
        # print('zdkgh')
        # symbolsss = self.get_top_coins_template()
        # print(symbolsss)
        # return
        # //////////////////////////////
        # self.last_message.text = self.connector_func(self.last_message, f"Hello Denis! Your marketplace is: <<{self.market_place}>> May God blass you!!")
        print(f"Hello {self.my_name}!\nYour marketplace is: <<{self.market_place.upper()}>>\nYour type market is: <<{self.market_type.upper()}>>\nMay God blass you!!")
        # //////////////////////////////
        self.run_flag = True
        response_trading_total_list = []   
        in_position = False     
        create_order_success_flag = False 
        stop_loss_ratio = None  
        target_price = None   
        # //////////////////////////////////
        print("set default margin_type:")
        set_margin_resp = self.set_margin_type(self.symbol, self.margin_type)
        print(set_margin_resp)
        print("set default leverage:")
        set_leverage_resp = self.set_leverage(self.symbol, self.lev_size)
        print(set_leverage_resp)
        # ////////////////////////////////////////////////////////////
        while True:
            self.default_pre_trading_vars()
            if self.stop_bot_flag:
                self.last_message.text = self.connector_func(self.last_message, "EMA bot was stoped!")
                print("EMA bot was stoped!")
                self.run_flag = False
                return
            # //////////////////////////////////////////////////////////////////////
            time.sleep(5) # test
            ### self.wait_time = self.time_calibrator(self.kline_time, self.time_frame)
            self.wait_time = self.time_calibrator(1, self.time_frame) #- проверять сигнал каждую минуту
            # print(f"Ожидание {self.wait_time} секунд до следующего временного интервала...")         
            await asyncio.sleep(self.wait_time) 
            # //////////////////////////////////////////////////////////////////////
            self.get_signal_val = await self.get_signal_shell()
            # # # /////////// test:
            # self.cur_klines_data = self.get_klines(self.symbol)
            # self.get_signal_val = "LONG_SIGNAL"
            # self.get_signal_val = "SHORT_SIGNAL"
            # # # ///////////////////////////////////////////
            if self.get_signal_val:                
                # self.last_message.text = self.connector_func(self.last_message, self.get_signal_val)
                print(self.get_signal_val)
                self.cur_price, self.qty = self.pre_trading_info_template()
                # /////////////////// create order logic//////////////////////////////
                self.direction = 1 if self.get_signal_val == "LONG_SIGNAL" else -1                                      
                self.response_trading_list, create_order_success_flag = self.make_orders_template(self.qty, 'MARKET', None)             
                response_trading_total_list += self.response_trading_list
                # create_order_success_flag = True # test              
                # /////////////////// create order logic//////////////////////////////                
                if create_order_success_flag:
                    create_order_success_flag = False                    
                    print(self.response_trading_list)
                    # //////////////////////////////////////////////////////////////////
                    self.enter_price, self.executed_qty = self.post_trading_info_template(self.response_trading_list, self.qty, self.cur_price)                     
                    # /////////////////////////////////////////////////////////////////////
                    stop_loss_ratio = self.calculate_stop_loss_ratio(self.direction, self.enter_price, self.cur_klines_data, self.stop_loss_type, self.default_stop_loss_ratio_val)  
                    print(f"stop_loss_ratio: {stop_loss_ratio}") 
                    # устанавливаем фиксированный стоп лосс ордер в качестве подстраховки:
                    target_price = self.enter_price* (1 - self.direction*stop_loss_ratio)
                    self.direction = self.direction*(-1)
                    self.response_trading_list, create_order_success_flag = self.make_orders_template(self.qty, 'STOP_MARKET', target_price)             
                    response_trading_total_list += self.response_trading_list
                    self.direction = self.direction*(-1)
                    if self.stop_loss_global_type == 'TRAILLING_GLOBAL_TYPE':
                        self.stop_order_total_multipliter = await self.stop_logic_price_monitoring(self.symbol, self.direction, self.enter_price, stop_loss_ratio)
                        stop_loss_ratio = None
                        # self.stop_order_total_multipliter = 0 # test
                        print(f"stop_order_total_multipliter: {self.stop_order_total_multipliter}")
                        if self.stop_order_total_multipliter is not None:                            
                            if not self.is_open_position_true(self.symbol):                        
                                print("The current position probably was closed manualy or as result some others anomaly...")
                                self.default_post_trading_vars()
                                # return # test
                                continue
                            print("Position is avialable yet")
                            self.is_closing = -1
                            self.response_trading_list, self.close_position_success_flag = self.make_orders_template(self.executed_qty)
                            response_trading_total_list += self.response_trading_list
                            if self.close_position_success_flag:
                                show_post_trade_info_answer = self.show_post_trade_info(self.stop_order_total_multipliter)   
                                print(show_post_trade_info_answer)                             
                                self.default_post_trading_vars()                         
                            else:
                                print('Some problems with closing position...')                            
                        else:
                            print("Stop_logic_price_monitoring func was finished uncorrectly...")
                    elif self.stop_loss_global_type == 'FIXED_GLOBAL_TYPE':
                        target_price = self.enter_price* (1 + self.direction*stop_loss_ratio)
                        self.direction = self.direction*(-1)
                        self.response_trading_list, create_order_success_flag = self.make_orders_template(self.qty, 'TAKE_PROFIT_MARKET', target_price)             
                        response_trading_total_list += self.response_trading_list
                        self.direction = self.direction*(-1)

            else:
                print("NO_SIGNAL")
            # return # test
            # ///////////////////////////////////////////////////////////////////////////

if __name__=="__main__": 
    asyncio.run(MAIN_CONTROLLER().main_func())
    # print('Please go to the Telegram bot interface!')     
    # bot = TG_MANAGER()   
    # bot.run()
