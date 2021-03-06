import os
import json
from google.cloud import datastore


def get_from_datastore(config_key, env):
    ds = datastore.Client()
    print("Fetching {}".format(config_key))

    product_key = ds.key("Settings", env)
    entity = ds.get(product_key)

    return entity[config_key]


CONFIG_ENV = os.getenv("CONFIG_ENV", 'production')
PROJECT_ID = os.getenv("PROJECT_ID", "kryptos-205115")
PLATFORM_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(PLATFORM_DIR)
PERF_DIR = os.path.join(BASE_DIR, "performance_results")
LOG_DIR = os.path.join(BASE_DIR, "logs")

REDIS_HOST = os.getenv("REDIS_HOST", "10.0.0.3")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)

SENTRY_DSN = os.getenv("SENTRY_DSN", None)

CLOUD_LOGGING = os.getenv('CLOUD_LOGGING', False)

REMOTE_BASE_URL = "https://kryptos-205115.appspot.com"
LOCAL_BASE_URL = "http://web:8080"

if CONFIG_ENV == 'dev':
    WEB_URL = LOCAL_BASE_URL
else:
    WEB_URL = REMOTE_BASE_URL


STRAT_DIR = os.path.join(PLATFORM_DIR, "strategy")
DEFAULT_CONFIG_FILE = os.path.join(STRAT_DIR, "config.json")


QUEUE_NAMES = ["paper", "live", "backtest", "ta"]

with open(DEFAULT_CONFIG_FILE, "r") as f:
    DEFAULT_CONFIG = json.load(f)


# Optionally set metrics here instead of with the metrics "-m" option
METRICS = [
    # 'algo_volatility',
    "alpha",
    # 'benchmark_period_return',
    # 'benchmark_volatility',
    "beta",
    # 'gross_leverage',
    # 'long_exposure',
    # 'long_value',
    # 'longs_count',
    "max_drawdown",
    # 'max_leverage',
    # 'net_leverage',
    "pnl",
    "sharpe",
    # 'short_exposure',
    # 'short_value',
    # 'shorts_count',
    "sortino",
]


# Technical Analysis Settings
class TAConfig(object):

    # global
    BARS = 365
    ORDER_SIZE = 0.01
    SLIPPAGE_ALLOWED = 0.05

    # bbands.py
    # MATYPE = ta.MA_Type.T3
    SAR_ACCEL = 0.02
    SAR_MAX = 0.2

    # macdfix.py
    MACD_SIGNAL = 9
    RSI_OVERSOLD = 55
    RSI_OVERBOUGHT = 65

    # mean_reversion.py
    # RSI_OVERSOLD = 55     # defined in macdfix section
    # RSI_OVERBOUGHT = 65   # defined in macdfix section
    CANDLE_SIZE = "5T"

    # rsi_profit_target.py
    MAX_HOLDINGS = 0.2
    # RSI_OVERSOLD = 30     # defined in macdfix section
    RSI_OVERSOLD_BBANDS = 45
    RSI_OVERBOUGHT_BBANDS = 55
    TARGET = 0.15
    STOP_LOSS = 0.1
    STOP = 0.03

    # rsi_ta.py
    RSI_PERIOD = 7
    RSI_OVER_BOUGHT = 70
    RSI_OVER_SOLD = 30
    RSI_AVG_PERIOD = 15

    # sma_crossover.py
    # sma_macd.py
    SMA_FAST = 5503.84
    SMA_SLOW = 4771.08
    MACD_FAST = 12
    MACD_SLOW = 26
    # MACD_SIGNAL = 9   # defined in macdfix

    # stoch_rsi.py
    TIMEPERIOD = 9
    FASTK_PERIOD = 5
    FASTD_PERIOD = 3
    FASTD_MATYPE = 0
    # STOCH_OVER_BOUGHT = 20    # defined in stochastics section
    # STOCH_OVER_SOLD = 80      # defined in stochastics section

    # stochastics.py
    STOCH_K = 14
    STOCH_D = 3

    STOCH_OVERBOUGHT = 80
    STOCH_OVERSOLD = 20
