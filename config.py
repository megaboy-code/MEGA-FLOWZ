# ===============================================================
# ⚙️ CONFIGURATION SETTINGS - UPDATED FOR AUTO-START
# ===============================================================

# Available trading symbols
AVAILABLE_SYMBOLS = [
    "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD",
    "NZDUSD", "XAUUSD", "BTCUSD", "ETHUSD", "XRPUSD"
]

# Symbol suffixes to try
SYMBOL_SUFFIXES = ["", "m", "c"]

# MT5 Timeframe mappings
TIMEFRAME_MT5_MAPPING = {
    "M1": 1, "M5": 5, "M15": 15, "H1": 60, "H4": 240, "D1": 1440
}

# Pyramid style configurations - UPDATED FOR DASHBOARD
PYRAMID_STYLES = {
    'scalper': ("⚡ Scalper", ["M15", "M5", "M1"]),
    'intraday': ("📈 Intraday", ["H1", "M15", "M5", "M1"]),
    'swing': ("🔄 Swing", ["H4", "H1", "M15", "M5", "M1"]),
    'daily': ("📅 Daily", ["D1", "H4", "H1", "M15", "M5", "M1"])  # Default
}

# All available timeframes for internal fetching
ALL_TIMEFRAMES = ["D1", "H4", "H1", "M15", "M5", "M1"]

# Timeframe durations in minutes
TIMEFRAME_DURATIONS = {
    "D1": 1440, "H4": 240, "H1": 60, "M15": 15, "M5": 5, "M1": 1
}

# Default settings - UPDATED FOR AUTO-START
DEFAULT_SETTINGS = {
    'symbol': 'EURUSD',           # Auto-start with EURUSD
    'pyramid_style': 'daily',     # Default to Daily pyramid
    'fetch_interval': 30,         # 30 seconds default
    'extract_count': 10,
    'dashboard_port': 5000,
    'candle_count': 200,          # Unified: 200 candles for all timeframes
    'utc_offset': 0,              # UTC+0 default
    'auto_suffix': True           # Auto-detect symbol suffixes
}

# Chart configuration
CHART_CONFIG = {
    'timeframe_minutes': {"M1": 1, "M5": 5, "M15": 15, "H1": 60, "H4": 240, "D1": 1440},
    'time_range_formats': {
        "M1": "%H:%M", "M5": "%H:%M", "M15": "%H:%M",
        "H1": "%H:%M", "H4": "%H:%M", "D1": "%Y-%m-%d"
    }
}

# Technical indicators configuration - NEW
TECHNICAL_INDICATORS = {
    'RSI': {'period': 14, 'overbought': 70, 'oversold': 30},
    'EMA': {'fast': 12, 'slow': 26},
    'SMA': {'fast': 20, 'slow': 50},
    'MACD': {'fast': 12, 'slow': 26, 'signal': 9},
    'BB': {'period': 20, 'std': 2}
}

# Theme configurations - NEW
THEMES = {
    'default': {
        'name': 'Default Dark',
        'bg': '#000000',
        'card': '#0A0A0A', 
        'text': '#FFFFFF',
        'accent': '#0066FF',
        'grid': '#1A1A1A',
        'border': '#333333'
    },
    'professional': {
        'name': 'Professional',
        'bg': '#121212',
        'card': '#1E1E1E',
        'text': '#E0E0E0',
        'accent': '#BB86FC',
        'grid': '#2A2A2A',
        'border': '#333333'
    },
    'terminal': {
        'name': 'Trading Terminal',
        'bg': '#001100',
        'card': '#002200',
        'text': '#00FF00',
        'accent': '#00FF88',
        'grid': '#003300',
        'border': '#004400'
    }
}