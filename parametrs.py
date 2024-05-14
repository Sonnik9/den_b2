import os
import math
from dotenv import load_dotenv
load_dotenv()

class PARAMS():
    def __init__(self) -> None:
        self.SOLI_DEO_GLORIA = 'Soli Deo Gloria!' # одному Богу слава!!
        # ///////////// интрадакшн ///////////////////////////////////
        self.init_all_params()

    def init_all_params(self):
        self.my_name = 'Nikolas' # ваше имя
        self.market_place = 'binance' # ...
        self.market_type = 'futures' # ...
        # /////////////////////////////////////////
        # self.in_position = False
        # //////////урлы api бинанс: ///////////////////////
        self.create_order_url = 'https://fapi.binance.com/fapi/v1/order'
        self.exchangeInfo_url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
        self.klines_url = 'https://fapi.binance.com/fapi/v1/klines' 
        self.set_margin_type_url = 'https://fapi.binance.com/fapi/v1/marginType'
        self.set_leverage_url = 'https://fapi.binance.com/fapi/v1/leverage'
        self.positions_url = 'https://fapi.binance.com/fapi/v2/positionRisk'
        self.all_tikers_url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
        self.get_all_orders_url = 'https://fapi.binance.com/fapi/v1/allOrders'
        # self.cancel_all_orders_url = 'https://fapi.binance.com/fapi/v1/allOpenOrders'
        # self.current_price_url = "https://fapi.binance.com/fapi/v1/ticker/price"
        # self.get_all_open_orders_url = 'https://fapi.binance.com/fapi/v1/openOrders'
        # self.account_url = 'https://fapi.binance.com/fapi/v2/account'
        # ////////////////////// некоторые переменные /////////////////////////////////////////
        self.cur_klines_data = None
        self.direction = None        
        # ////////////////////////////////////
        self.trading_must_have_settings()
        self.filter_settings()
        self.stop_loss_settings()
        self.ema_settings()
        self.default_statistic_vars()
        self.martin_gale_settings()
        self.default_tg_vars()
        self.init_keys()

    def trading_must_have_settings(self):
        # крипто пара:
        # self.symbol = 'BTCUSDT' 
        # self.symbol = 'ARBUSDT' 
        # self.symbol = 'BNBUSDT'
        self.symbol = 'DOGEUSDT'
        self.start_depo = 10 # начальное значение депо которое сбрасфывается после тог как текущий self.cur_martin_gale_multiplier достигнет максимального self.max_martin_gale_multiplier (см. настройки мартингейла)
        self.depo = 10 # депозит в USDT
        self.lev_size = 1 # размер кредитного плеча
        self.margin_type = 'ISOLATED' # CROSS (изолированная маржа или кросс маржа. Изолированная по дефолту)  

    def filter_settings(self):
        self.problem_pairs = ['shitok1', 'shitok2'] # монеты исключени. Например ['shitokusdt', 'shitok2usdt']
        self.price_filter_flag = False # фильтр по цене. Сейчас отключен. Включить True
        self.MIN_FILTER_PRICE = 0 # минимальный порог цены. Актуально если self.price_filter_flag = True
        self.MAX_FILTER_PRICE = math.inf # максимальный порог цены 
        self.daily_filter_direction = 0 # 0 -- пас. 1 -- искать только которые показывают растущую динамику (зеленые графики). -1 --- для падающих (красные графики) на бинанс
        self.slice_volum_flag = True # флаг фильтра по объему
        self.slice_volatilyty_flag = True # находить самые волатильные на бинанс
        self.SLICE_VOLATILITY = 30
        self.min_volume_usdtFilter_flag = False # искать по минимальному объему торгов за сутки на бинанс. False -- неактивный
        self.MIN_VOLUM_USDT = 10000000 # размер минимального обьема в usdt
        self.SLICE_VOLUME_BINANCE_PAIRS = 60 # срез монет по объему торгов на бинанс
        self.TOP_MARKET_CUP = 20 # срез монет. по коин маркет кап это будет первая двадцатка

    def stop_loss_settings(self):
        # /////////////////////////////////////////////////////
        self.stop_loss_global_type = 'TRAILLING_GLOBAL_TYPE' # треллинг стоп лосс 
        # self.stop_loss_global_type = 'FIXED_GLOBAL_TYPE' # фиксированные стоп лосс и тейк профит
        # ниже параметры для расчета stop_loss_ratio (stop_loss_ratio = abs(точка входа - точка стоп лосса)/ точка входа):
        self.ricks_earnings_ratio = '1:3' # соотношение риска к прибыли. только для 'FIXED_GLOBAL_TYPE'
        # //////// способы вычисления точки стоп лосса: /////////////////
        # self.stop_loss_type = 'LAST_MIN' # стоп лосс по последнуму локальному минимуму или максимуму
        self.stop_loss_type = 'ABSOLUTE_MIN' # стоп лосс по минимуму или максимуму за определенный период. Берется период равный длине наибольшего периода ema
        # self.stop_loss_type = 'ATR_VAL' # стоп лосс по волатильности умноженный на 1.6
        # self.stop_loss_type = 'FIXED' # фиксированный стоп. Может быть как в 'TRAILLING_GLOBAL_TYPE' так и в 'FIXED_GLOBAL_TYPE'
        self.default_stop_loss_ratio_val = 0.01 # дефолтное значение stop_loss_ratio для self.stop_loss_type = 'FIXED' или в результате аномалий при вычислении stop_loss_ratio
        # /////////////////////////////////////////////////////

    def ema_settings(self):
        self.kline_time, self.time_frame = 5, 'm' # таймфрейм где челое число - период, а буква - сам тайм фрейм (минута, час и т.д)
        self.interval = str(self.kline_time) + self.time_frame # то же только на китайский мови...
        self.strategy_name = 'ema_crossover_2x' # стратегия прересечения двух ema
        # self.strategy_name = 'ema_crossover_3x' # стратегия прересечения трех ema
        self.ema1_period = 5 # - длина короткой волны
        self.ema2_period = 10 # - длина длинной волны (для 'ema_crossover_3x' длина средней волны)
        self.ema3_period = None # для 'ema_crossover_2x' установлен в пустое значение. Для 'ema_crossover_3x' обязаня быть челым числом большим чем предыдущие две волны например 25
        self.ema_list = [self.ema1_period, self.ema2_period, self.ema3_period] # - для тех части...
        self.smoothing_crossover_condition = False # рекомендуется в False. Некое сглаживающие условия для нахождения сигнала. Потенциально может дать больше сигналов, но худшего качества. По желанию True

    def default_statistic_vars(self):
        self.show_statistic_hour = 21 # время показа дневной статистики (21 - в 9 часов вечера каждого дня)
        self.win_los = 0 # результат последней сделки (в плюс или в минус)
        # self.win_count = 0 # количество побед
        # self.loss_count = 0 # количество неудач
        # self.win_per = 0 # % побед
        # self.loss_per = 0 # % неудач
        self.daily_trade_history_list = [] # список трейдов (точки входа и точки выхода в позиции) за все время торгов
        self.total_trade_history_list = [] # список трейдов (точки входа и точки выхода в позиции) за все время торгов
        # self.max_profit_abs = 0 # макс прибыль в usdt
        # self.max_drawdown_abs = 0 # макс просадка в usdt
        # self.total_profit_abs = 0 # итоговый профит в usdt
        # self.total_losses_abs = 0 # итоговая просадка в usdt
        # self.profitable_unprofitable_ratio = 0 # соотношение прибыльных сделок к убыточным в %

    def martin_gale_settings(self):
        self.martin_gale_flag = False # мартин гейл отключен. Включить: self.martin_gale_flag = False
        self.martin_gale_ratio = 2 # множитель депозита
        self.cur_martin_gale_counter = 0 # всегда равен 0
        self.max_martin_gale_level = 4 # сколько раз умножать позицию

    # /////////// переменные... - суто по тех части: ///////////////////////
    def default_tg_vars(self): 
        self.run_flag = False
        self.stop_bot_flag = False          
        self.block_acess_flag = False
        self.start_flag = False
        self.start_day_date = None
        self.block_acess_counter = 0
        self.seq_control_flag = False
        self.seq_control_token = False
        self.stop_redirect_flag = False  
        self.settings_redirect_flag = False

    def init_keys(self): 
        # ////////////////////// инициализация ключей: ///////////////////////////////
        self.api_key  = os.getenv(f"{self.market_place.upper()}_API_PUBLIC_KEY", "")
        self.api_secret = os.getenv(f"{self.market_place.upper()}_API_PRIVATE_KEY", "")
        self.tg_api_token = os.getenv("TG_TOKEN", "")
        print(self.tg_api_token)
        self.coinMarketCup_api_token = os.getenv("COIN_MARKET_CUP_TOKEN", "")
        self.seq_control_token = os.getenv("ACESS_TOKEN", "")