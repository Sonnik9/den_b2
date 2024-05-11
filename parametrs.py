import os
import math
from dotenv import load_dotenv
load_dotenv()

class PARAMS():
    def __init__(self) -> None:
        self.SOLI_DEO_GLORIA = 'Soli Deo Gloria!' # одному Богу слава!!
        # ///////////// интрадакшн ///////////////////////////////////
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
        # self.current_price_url = "https://fapi.binance.com/fapi/v1/ticker/price"
        # self.get_all_orders_url = 'https://fapi.binance.com/fapi/v1/openOrders'
        # self.cancel_all_orders_url = 'https://fapi.binance.com/fapi/v1/allOpenOrders'
        # self.account_url = 'https://fapi.binance.com/fapi/v2/account'
        # ////////////////////// некоторые переменные /////////////////////////////////////////
        self.cur_klines_data = None
        self.direction = None 
        # ////////////////////////////////////
        self.trading_must_have_settings()
        self.filter_settings()
        self.stop_loss_settings()
        self.ema_settings()
        self.default_tg_vars()
        self.init_keys()

    def trading_must_have_settings(self):
        # крипто пара:
        # self.symbol = 'BTCUSDT' 
        # self.symbol = 'ARBUSDT' 
        # self.symbol = 'BNBUSDT'
        self.symbol = 'DOGEUSDT'
        self.depo = 10 # депозит в USDT
        self.lev_size = 1 # размер кредитного плеча
        self.margin_type = 'ISOLATED' # CROSS (изолированная маржа или кросс маржа. Изолированная по дефолту)  

    def filter_settings(self):
        self.problem_pairs = ['shitok1', 'shitok2'] # монеты исключени. Например ['shitokusdt', 'shitok2usdt']
        self.price_filter_flag = False # фильтр по цене. Сейчас отключен. Включить True
        self.MIN_FILTER_PRICE = 0 # минимальный порог цены. Актуально если self.price_filter_flag = True
        self.MAX_FILTER_PRICE = math.inf # максимальный порог цены 
        self.daily_filter_direction = 0 # 0 -- пас. 1 -- искать только которые показывают растущую динамику (зеленые графики). -1 --- для падающих (красные графики) на бинанс
        self.slice_volatilyty_flag = True # находить самые волатильные на бинанс
        self.SLICE_VOLATILITY = 50
        self.min_volume_usdtFilter_flag = False # искать по минимальному объему торгов за сутки на бинанс. False -- неактивный
        self.MIN_VOLUM_USDT = 10000000 # размер минимального обьема в usdt
        self.SLICE_VOLUME_BINANCE_PAIRS = 30 # срез монет по объему торгов на бинанс
        self.TOP_MARKET_CUP = 10 # срез монет. по коин маркет кап это будет первая двадцатка

    def stop_loss_settings(self):
        # /////////////////////////////////////////////////////
        self.stop_loss_global_type = 'TRAILLING_GLOBAL_TYPE' # треллинг стоп лосс 
        # self.stop_loss_global_type = 'FIXED_GLOBAL_TYPE' # фиксированные стоп лосс и тейк профит
        # ниже параметры для расчета stop_loss_ratio (stop_loss_ratio = abs(точка входа - точка стоп лосса)/ точка входа):
        self.ricks_earnings_ratio = '1/3' # соотношение риска к прибыли. только для 'FIXED_GLOBAL_TYPE'
        # //////// способы вычисления точки стоп лосса: /////////////////
        self.stop_loss_type = 'LAST_MIN' # стоп лосс по последнуму локальному минимуму или максимуму
        # self.stop_loss_type = 'ABSOLUTE_MIN' # стоп лосс по минимуму или максимуму за определенный период. Берется период равный длине наибольшего периода ema
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
        self.api_key = BINANCE_API_PUBLIC_KEY = "vcn37RFPQUOE9IH9DOjNFQEnbd51dAFCNiw2IURVX8ThdqjhfgkLwspkcL1WhxK1"
        self.api_secret = BINANCE_API_PRIVATE_KEY = "4WVbc7ATSwOBfCKUOh44KUuFhvJyiXdA63Oo1rYop5AQlJUiCmGj0kng6G1ds8Nf" 
        self.tg_api_token = TG_TOKEN = "7113130467:AAEC09EcS4qUA9FmkbpxwrKdSbfEeqrhS9Q"
        self.coinMarketCup_api_token = COIN_MARKET_CUP_TOKEN = "15dc358f-b26f-4200-8ee9-7f60b143480a"
        self.seq_control_token = ACESS_TOKEN = "d"
        # self.api_key  = os.getenv(f"{self.market_place.upper()}_API_PUBLIC_KEY", "")
        # self.api_secret = os.getenv(f"{self.market_place.upper()}_API_PRIVATE_KEY", "")
        # self.tg_api_token = os.getenv("TG_TOKEN", "")
        # self.coinMarketCup_api_token = os.getenv("COIN_MARKET_CUP_TOKEN", "")
        # self.seq_control_token = os.getenv("ACESS_TOKEN", "")