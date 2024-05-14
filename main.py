import telebot
from telebot import types 
import time
import math
# import random
# import asyncio
# import aiohttp
# import json
# import decimal
# from datetime import datetime
from risk_management import STATISTIC
from utils import UTILS, COIN_MARKET_API_PARSER
from risk_management import STOP_LOGIC
from log import total_log_instance, log_exceptions_decorator

class CONNECTOR_TG(STATISTIC, UTILS, COIN_MARKET_API_PARSER, STOP_LOGIC):
    def __init__(self):  
        super().__init__()  
        self.bot = telebot.TeleBot(self.tg_api_token)
        self.menu_markup = self.create_menu() 
        self.last_message = None

    def create_menu(self):
        menu_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        button1 = types.KeyboardButton("START")
        button2 = types.KeyboardButton("STOP")
        button3 = types.KeyboardButton("SEARCH_COINS")
        button4 = types.KeyboardButton("SETTINGS")    
        menu_markup.add(button1, button2, button3, button4)        
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
        order_answer = {}
        response_list = []        
        side = 'BUY' if self.direction == 1 else 'SELL'
        try:
            order_answer = self.make_order(self.symbol, qty, side, market_type, target_price)
            response_list.append(order_answer)
        except Exception as ex:
            print(ex)
        return response_list, self.response_order_logger(order_answer, side, market_type)
    
    @log_exceptions_decorator
    def make_tralling_sl_template(self, qty, stop_loss_ratio):
        order_answer = None
        side = 'BUY' if self.direction == -1 else 'SELL'
        callbackRate = round(stop_loss_ratio*100, 2)
        if callbackRate < 0.1:
            print("callbackRate < 0.1")
            callbackRate = 0.1 # в % для трелинг стоп лосса
        try:
            order_answer = self.tralling_stop_order(self.symbol, qty, side, callbackRate)            
        except Exception as ex:
            print(ex)
        return self.response_order_logger(order_answer, side, 'TRAILING_STOP_MARKET')
    
    @log_exceptions_decorator
    def make_sl_tp_template(self, qty, market_type_list, target_price_list):
        order_answer = None
        response_success_list = []
        side = 'BUY' if self.direction == -1 else 'SELL'
        for market_type, target_price in zip(market_type_list, target_price_list):
            try:
                order_answer = self.make_order(self.symbol, qty, side, market_type, target_price)
                response_success_list.append(self.response_order_logger(order_answer, side, market_type))
                time.sleep(0.1)
            except Exception as ex:
                print(ex)
        return all(response_success_list)
    
    def pre_trading_info_template(self):
        symbol_info = self.get_excangeInfo() 
        self.cur_klines_data = self.get_klines(self.symbol) 
        cur_price = self.cur_klines_data['Close'].iloc[-1]
        qty, price_precession = self.usdt_to_qnt_converter(self.symbol, self.depo, symbol_info, cur_price)
        print("qty, cur_price:")
        self.last_message.text = self.connector_func(self.last_message, "qty, cur_price:")
        self.last_message.text = self.connector_func(self.last_message, f"{qty}, {price_precession}") 
        self.from_anomal_view_to_normal([qty, cur_price]) 
        return cur_price, qty, price_precession   
    
    def post_open_true_info_template(self, response_trading_list, qty, cur_price):
        # //////////////////////////////////////////////////////////////////
        executed_qty = float(response_trading_list[0].get('executedQty', qty))
        enter_price = float(response_trading_list[0].get('avgPrice', cur_price)) 
        order_id = response_trading_list[0].get('orderId', None)
        print("qty, enter_price:")
        self.last_message.text = self.connector_func(self.last_message, "qty, enter_price:")
        self.last_message.text = self.connector_func(self.last_message, f"{executed_qty}, {enter_price}") 
        self.from_anomal_view_to_normal([executed_qty, enter_price])  
        return enter_price, executed_qty 
    
    def post_trade_info_viwer(self, last_signal, last_win_los):
        post_trade_piece_message = ""
        if last_signal == 'LONG_SIGNAL':
            post_trade_piece_message = 'Лонговая' 
        elif last_signal == 'SHORT_SIGNAL':
            post_trade_piece_message = 'Шортовая' 
        print(f"{post_trade_piece_message} позиция была закрыта")
        self.last_message.text = self.connector_func(self.last_message, f"{post_trade_piece_message} позиция была закрыта") 
               
        if last_win_los == 1:
            print(f"Последняя {post_trade_piece_message} сделка была закрыта в плюс")  
            self.last_message.text = self.connector_func(self.last_message, f"Последняя {post_trade_piece_message} сделка была закрыта в плюс") 
        elif last_win_los == -1:
            print(f"Последняя {post_trade_piece_message} сделка была закрыта в минус") 
            self.last_message.text = self.connector_func(self.last_message, f"Последняя {post_trade_piece_message} сделка была закрыта в минус")    
        else:
            print(f"Bo время попытки проанализировать последнюю сделку возникли какие то трудности. Рекомундуем войти в интерфейс фьючерсной торговли вашего приложения Binance и проверить ситуацию. Скоро бот будет остановлен")
            self.last_message.text = self.connector_func(self.last_message, f"Bo время попытки проанализировать последнюю сделку возникли какие то трудности. Рекомундуем войти в интерфейс фьючерсной торговли вашего приложения Binance и проверить ситуацию. Скоро бот будет остановлен") 
            return False
        return True
    
    def response_order_logger(self, order_answer, side, market_type): 
        if order_answer is not None:  
            if order_answer['status'] == 'FILLED' or order_answer['status'] == 'NEW':
                print(f'{side} позиция {market_type} типа была открыта успешно!')
                self.last_message.text = self.connector_func(self.last_message, f'{side} позиция {market_type} типа была открыта успешно!') 
                self.last_message.text = self.connector_func(self.last_message, str(order_answer))
                return True
            elif order_answer['status'] == 'PARTIALLY_FILLED':
                print(f'{side} позиция {market_type} типа была открыта co статусом PARTIALLY_FILLED')
                self.last_message.text = self.connector_func(self.last_message, f'{side} позиция {market_type} типа была открыта co статусом PARTIALLY_FILLED') 
                self.last_message.text = self.connector_func(self.last_message, str(order_answer))
                return True
        print(f'{side} позиция {market_type} типа не была открыта...')
        self.last_message.text = self.connector_func(self.last_message, f'{side} позиция {market_type} типа не была открыта...') 
        self.last_message.text = self.connector_func(self.last_message, str(order_answer))
        return False
    
    def martin_gale_regulator(self, last_win_los):
        if self.cur_martin_gale_counter == self.max_martin_gale_level:
            self.cur_martin_gale_counter = 0
            self.depo = self.start_depo
            return False
        if last_win_los == -1:                        
            self.depo = round(self.depo*self.martin_gale_ratio, 2)
            self.cur_martin_gale_counter += 1
        elif last_win_los == 1: 
            if self.cur_martin_gale_counter != 0:
                self.cur_martin_gale_counter -= 1
                self.depo = round(self.depo/self.martin_gale_ratio, 2)
        # if self.depo < self.start_depo:
        #     self.depo = self.start_depo
        return True
        
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
                if self.slice_volum_flag:
                    top_pairs = sorted(top_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
                    top_pairs = top_pairs[:self.SLICE_VOLUME_BINANCE_PAIRS]

                if self.min_volume_usdtFilter_flag:
                    top_pairs = [x for x in top_pairs if float(x['quoteVolume']) >= self.MIN_VOLUM_USDT]

                if self.slice_volatilyty_flag:
                    top_pairs = sorted(top_pairs, key=lambda x: abs(float(x['priceChangePercent'])), reverse=True)
                    top_pairs = top_pairs[:self.SLICE_VOLATILITY]
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
    def set_leverage_template(self):
        print("Устанавливаем кредитное плечо:")
        self.last_message.text = self.connector_func(self.last_message, "Устанавливаем кредитное плечо:")
        # print(self.symbol, self.lev_size)
        set_leverage_resp = self.set_leverage(self.symbol, self.lev_size)
        print(set_leverage_resp)
        self.last_message.text = self.connector_func(self.last_message, str(set_leverage_resp))
        return True 

    @log_exceptions_decorator
    def get_signal_shell(self): 
        self.cur_klines_data = self.get_klines(self.symbol)
        return self.get_signals(self.strategy_name, self.smoothing_crossover_condition, self.cur_klines_data, self.ema1_period, self.ema2_period)
  
    @log_exceptions_decorator
    def main_func(self):       
        if self.martin_gale_flag:
            print("Мартин Гейл включен")
            self.last_message.text = self.connector_func(self.last_message, "Мартин Гейл включен")               
        else:
            print("Мартин Гейл отключен")
            self.last_message.text = self.connector_func(self.last_message, "Мартин Гейл отключен")
        # //////////////////////////////
        self.run_flag = True
        in_position = False     
        create_order_success_flag = False 
        last_signal = None
        is_show_statistic_true = False
        next_show_statistic_time = self.get_next_show_statistic_time()  
        last_win_los = 0
        init_order_price, oposit_order_price = 0, 0
        last_depo = 0     
        # //////////////////////////////////
        print("Устанавливаем тип маржи:")
        self.last_message.text = self.connector_func(self.last_message, "Устанавливаем тип маржи:")
        set_margin_resp = self.set_margin_type(self.symbol, self.margin_type)
        print(set_margin_resp)
        self.last_message.text = self.connector_func(self.last_message, str(set_margin_resp))
        self.set_leverage_template()        
        # ////////////////////////////////////////////////////////////
        while True:
            self.cur_klines_data = None
            get_signal_val = None
            if self.stop_bot_flag:
                self.last_message.text = self.connector_func(self.last_message, "EMA bot was stoped!")
                print("EMA bot остановлен!")
                self.run_flag = False
                return
            # //////////////////////////////////////////////////////////////////////
            # ### wait_time = self.time_calibrator(self.kline_time, self.time_frame)
            # wait_time = self.time_calibrator(1, self.time_frame) #- проверять сигнал каждую минуту
            # # print(f"Ожидание {wait_time} секунд до следующего временного интервала...")         
            # await asyncio.sleep(wait_time)
            # time.sleep(wait_time) 
            # # //////////////////////////////////////////////////////////////////////
            # ## test:
            print("Следующая итерация")
            time.sleep(60) # test

            if not in_position:
                # get_signal_val = await self.get_signal_shell()
                # # # /////////// test:
                self.cur_klines_data = self.get_klines(self.symbol)
                get_signal_val = "LONG_SIGNAL"
                # get_signal_val = "SHORT_SIGNAL"                
                # # # ///////////////////////////////////////////
                if get_signal_val:                
                    # self.last_message.text = self.connector_func(self.last_message, get_signal_val)
                    print(get_signal_val)
                    self.last_message.text = self.connector_func(self.last_message, get_signal_val)
                    last_signal = get_signal_val
                    qty = None
                    cur_price = None
                    price_precession = None
                    self.direction = None
                    response_trading_list = None
                    cur_price, qty, price_precession = self.pre_trading_info_template()
                    # /////////////////// create order logic//////////////////////////////
                    self.direction = 1 if get_signal_val == "LONG_SIGNAL" else -1                                      
                    response_trading_list, create_order_success_flag = self.make_orders_template(qty, 'MARKET', None)             
                else:
                    # print("NO_SIGNAL")
                    # self.last_message.text = self.connector_func(self.last_message, "NO_SIGNAL")
                    continue 
            else:
                if not self.is_open_position_true(self.symbol):
                    in_position = False
                    # //////////// show statistic: ///////////////////////////////
                    last_win_los = 0
                    init_order_price, oposit_order_price = 0, 0
                    last_depo = 0
                    last_win_los, init_order_price, oposit_order_price, last_depo = self.last_statistic(self.symbol)  
                    self.daily_trade_history_list.append((last_win_los, init_order_price, oposit_order_price, last_depo))                  
                    if not self.post_trade_info_viwer(last_signal, last_win_los):
                        self.stop_bot_flag = True
                        continue                 

                    is_show_statistic_true, next_show_statistic_time = self.show_statistic_signal(next_show_statistic_time)
                    if is_show_statistic_true:
                        result_statistic_dict = {}
                        result_statistic_dict = self.statistic_calculations(self.daily_trade_history_list)
                        print(f"Показатели торгов за сутки:\n{result_statistic_dict}")
                        self.last_message.text = self.connector_func(self.last_message, f"Показатели торгов за сутки:\n{result_statistic_dict}")
                        self.daily_trade_history_list = []

                    # ////////////////// мартин гейл футкция: //////////////////////////////
                    if self.martin_gale_flag:
                        if not self.martin_gale_regulator(last_win_los):
                            print(f"Размер депозита был сброшен до начального и составляет: {self.depo}")
                            self.last_message.text = self.connector_func(self.last_message, f"Размер депозита был сброшен до начального и составляет: {self.depo}")
                            continue 
                        else:
                            print(f"Размер депозита был изменен и составляет: {self.depo}\n Tекущий Мартин Гейл счетчик равен {self.cur_martin_gale_counter}")
                            self.last_message.text = self.connector_func(self.last_message, f"Размер депозита был изменен и составляет: {self.depo}\n Tекущий Мартин Гейл счетчик равен {self.cur_martin_gale_counter}")
                    # ///////////////////////////////////////////////////////////////                   
                else:
                    # print("Позиция еще открыта")
                    continue
             
            if create_order_success_flag:
                in_position = True
                create_order_success_flag = False  
                executed_qty = None 
                enter_price = None 
                stop_loss_ratio = None                   
                # print(response_trading_list)
                # self.last_message.text = self.connector_func(self.last_message, str(response_trading_list))
                # //////////////////////////////////////////////////////////////////
                enter_price, executed_qty = self.post_open_true_info_template(response_trading_list, qty, cur_price)                     
                # /////////////////////////////////////////////////////////////////////
                stop_loss_ratio = self.calculate_stop_loss_ratio(self.direction, enter_price, self.cur_klines_data, self.stop_loss_type, self.default_stop_loss_ratio_val)  
                # print(f"stop_loss_ratio: {stop_loss_ratio}") 

                if self.stop_loss_global_type == 'TRAILLING_GLOBAL_TYPE':
                    if not self.make_tralling_sl_template(executed_qty, stop_loss_ratio):
                        print("Что-то пошло не так... закройте позицию вручную!!") 
                        self.last_message.text = self.connector_func(self.last_message, "Что-то пошло не так... закройте позицию вручную!!")                          
                        self.stop_bot_flag = True
                        continue          
                    
                elif self.stop_loss_global_type == 'FIXED_GLOBAL_TYPE':
                    target_sl_price = None
                    target_tp_price = None
                    tp_multipliter = float(self.ricks_earnings_ratio.split(':')[1].strip())
                    target_sl_price = round((enter_price* (1 - self.direction*stop_loss_ratio)), price_precession)
                    target_tp_price = round((enter_price* (1 + self.direction*stop_loss_ratio*tp_multipliter)), price_precession)
                    if not self.make_sl_tp_template(executed_qty, ['STOP_MARKET', 'TAKE_PROFIT_MARKET'], [target_sl_price, target_tp_price]):
                        print("Что-то пошло не так... закройте позицию вручную!!")  
                        self.last_message.text = self.connector_func(self.last_message, "Что-то пошло не так... закройте позицию вручную!!")  
                        self.stop_bot_flag = True
                        continue

class TG_MANAGER(MAIN_CONTROLLER):
    def __init__(self):
        super().__init__()  
        self.stop_redirect_flag = False  
        self.settings_redirect_flag = False    

    def run(self):  
        try: 
            @self.bot.message_handler(commands=['start'])
            @self.bot.message_handler(func=lambda message: message.text == 'START')
            def handle_start_input(message):
                if self.block_acess_flag:
                    response_message = "Это вам не пароль от вифи взламывать!!!"
                    message.text = self.connector_func(message, response_message)
                else:   
                    self.start_day_date = self.date_of_the_month()          
                    self.bot.send_message(message.chat.id, "Пожалуйста введите код доступа..", reply_markup=self.menu_markup)                   
                    self.start_flag = True

            @self.bot.message_handler(func=lambda message: self.start_flag)
            def handle_start_redirect(message):                
                try:
                    cur_day_date = None                    
                    value_token = message.text.strip()
                    cur_day_date = self.date_of_the_month()

                    if self.start_day_date != cur_day_date:
                        self.start_day_date = cur_day_date
                        self.block_acess_flag = False 
                        self.block_acess_counter = 0

                    if value_token == self.seq_control_token and not self.block_acess_flag:
                        self.seq_control_flag = True 
                        self.start_flag = False
                        self.stop_bot_flag = False
                        # ////////////////////////////////////////////////////////////////////
                        try:                                                       
                            response_message = f'Да благословит вас Бог {self.my_name}!'
                            # print(response_message) 
                            self.bot.send_message(message.chat.id, response_message, reply_markup=self.menu_markup)
                            self.last_message = message
                            if self.run_flag:
                                message.text = self.connector_func(message, "Сперва остановите робота ..")
                            else:
                                self.init_all_params()                                
                                self.main_func()  
                        except Exception as ex:
                            print(ex) 
                        # ////////////////////////////////////////////////////////////////////                       

                    elif value_token != self.seq_control_token and not self.block_acess_flag:                               
                        self.block_acess_counter += 1
                        if self.block_acess_counter >= 3:
                            self.block_acess_flag = True
                            self.start_flag = False 
                            response_message = "Попытки доступа исчерпаны. Попробуйте в другой раз"
                            message.text = self.connector_func(message, response_message)
                        else:
                            response_message = "Пожалуйста введите действителный код доступа"
                            message.text = self.connector_func(message, response_message)
                except Exception as ex:
                    print(ex)        
            # ////////////////////////////////////////////////////////////////////////////
            @self.bot.message_handler(func=lambda message: message.text == 'STOP')             
            def handle_stop(message):
                # if self.seq_control_flag and not self.block_acess_flag:\
                self.last_message = message
                self.bot.send_message(message.chat.id, "Остановить бота? (y/n)")
                self.stop_redirect_flag = True
                # else:
                #     self.bot.send_message(message.chat.id, "Нажмите START для верификации")

            @self.bot.message_handler(func=lambda message: self.stop_redirect_flag)             
            def handle_stop_redirect(message):
                self.last_message = message
                self.stop_redirect_flag = False
                if message.text.strip().upper() == 'Y':                    
                    self.stop_bot_flag = True 
                    self.bot.send_message(message.chat.id, "Немного подождите...")                   
                else:
                    self.bot.send_message(message.chat.id, "Бот не был остановлен...") 
            # /////////////////////////////////////////////////////////////////////////////// 
            @self.bot.message_handler(func=lambda message: message.text == 'SEARCH_COINS')             
            def handle_search_coins(message):
                self.last_message = message
                # if self.seq_control_flag and not self.block_acess_flag:
                candidate_symbols_list = self.get_top_coins_template()
                mess_resp = '\n'.join(candidate_symbols_list)
                self.bot.send_message(message.chat.id, mess_resp)
                # else:
                #     self.bot.send_message(message.chat.id, "Нажмите START для верификации")
            # ////////////////////////////////////////////////////////////////////////////
            @self.bot.message_handler(func=lambda message: message.text == 'SETTINGS')             
            def handle_settings(message):
                self.last_message = message
                # if self.seq_control_flag and not self.block_acess_flag:
                self.bot.send_message(message.chat.id, "Введите торговую пару, размер депозита (в usdt) и кредитное плечо. Например: btcusdt 20 2")
                self.settings_redirect_flag = True
                # else:
                #     self.bot.send_message(message.chat.id, "Нажмите START для верификации")

            @self.bot.message_handler(func=lambda message: self.settings_redirect_flag)             
            def handle_settings_redirect(message):
                self.last_message = message
                self.settings_redirect_flag = False
                dataa = [x for x in message.text.split(' ') if x and x.strip()]
                self.symbol = dataa[0].upper()  
                self.start_depo = self.depo = round(float(dataa[1]), 2)
                self.lev_size = int(float(dataa[2])) 
                # print(self.lev_size)
                # ///////////////////
                # self.init_all_params()
                self.bot.send_message(message.chat.id, f"Текущая торговая пара: {self.symbol}")
                self.bot.send_message(message.chat.id, f"Текущий депозит: {self.depo}")
                if self.set_leverage_template():
                    self.bot.send_message(message.chat.id, f"Текущее кредитное плечо: {self.lev_size}")
                else:
                    self.bot.send_message(message.chat.id, f"Не удалось установить кредитное плеч...")

 
            # /////////////////////////////////////////////////////////////////////////////// 
            # self.bot.polling()
            self.bot.infinity_polling()
        except Exception as ex: 
            print(ex)

if __name__=="__main__": 
    # asyncio.run(MAIN_CONTROLLER().main_func())
    # MAIN_CONTROLLER().main_func()
    print('Пожалуйста перейдите в интерфейс вашего телеграм бота!')     
    bot = TG_MANAGER()   
    bot.run()
