# =============================================================== 
# 🔌 MT5 CONNECTOR - DATA FETCHING MODULE - FIXED VERSION
# ===============================================================

import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import time
from typing import Dict, List, Optional
import config

class MT5Connector:
    def __init__(self):
        # Core configuration
        self.symbol = None
        self.timeframe = None
        self.utc_offset = 0
        self.quiet_mode = False
        self.timeframes = {}
        
        # MT5 state
        self.connected = False
        self.available_symbols = []
        
        print("🔌 MT5 Connector initialized")

    # ===========================================================
    # 🔗 MT5 CONNECTION MANAGEMENT
    # ===========================================================
    def initialize_mt5(self) -> bool:
        """Initialize MT5 connection"""
        if not mt5.initialize():
            raise Exception("❌ Failed to initialize MT5")
        if not self.quiet_mode:
            print("✅ Connected to MT5")
        self.connected = True
        self._load_available_symbols()
        return True

    def _load_available_symbols(self):
        """Load available symbols from MT5"""
        try:
            symbols = mt5.symbols_get()
            self.available_symbols = [s.name for s in symbols] if symbols else []
            print(f"📋 Loaded {len(self.available_symbols)} available symbols")
        except Exception as e:
            print(f"❌ Error loading symbols: {e}")

    def safe_shutdown(self):
        """Safely shutdown MT5 connection"""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            print("🔌 MT5 connection closed")

    # ===========================================================
    # 🎯 SYMBOL MANAGEMENT - FIXED VERSION
    # ===========================================================
    def detect_symbol_suffix(self, base_symbol: str) -> str:
        """Detect correct symbol suffix for broker"""
        # Remove any slashes for MT5 symbol format
        base_symbol = base_symbol.replace('/', '')
        
        if base_symbol in self.available_symbols:
            return base_symbol
            
        for suffix in config.SYMBOL_SUFFIXES:
            test_symbol = base_symbol + suffix
            if test_symbol in self.available_symbols:
                print(f"🔍 Detected symbol: {base_symbol} → {test_symbol}")
                return test_symbol
                
        for symbol in self.available_symbols:
            if base_symbol in symbol:
                print(f"🔍 Found similar: {base_symbol} → {symbol}")
                return symbol
                
        return base_symbol

    def verify_symbol(self, symbol: str) -> bool:
        """Verify symbol exists and is selected in MT5"""
        if not self.connected:
            return False
            
        # Ensure symbol is selected in MT5
        if not mt5.symbol_select(symbol, True):
            print(f"❌ Failed to select symbol: {symbol}")
            return False
            
        symbol_info = mt5.symbol_info(symbol)
        if not symbol_info:
            print(f"❌ Symbol info not available: {symbol}")
            return False
            
        print(f"✅ Symbol verified: {symbol}")
        return True

    # ===========================================================
    # ⚙️ AUTO-CONFIGURATION (NO USER INPUT) - FIXED VERSION
    # ===========================================================
    def configure_from_settings(self, settings: dict):
        """Configure connector from settings (no terminal input)"""
        base_symbol = settings.get('symbol', 'EURUSD')
        
        # Auto-detect symbol suffix but KEEP original symbol for cache
        if settings.get('auto_suffix', True):
            detected_symbol = self.detect_symbol_suffix(base_symbol)
            self.symbol = base_symbol  # FIXED: Keep ORIGINAL symbol for cache
            print(f"🔧 Configuring: {base_symbol} → {detected_symbol} (MT5), cache: {base_symbol}")
        else:
            self.symbol = base_symbol
            print(f"🔧 Configuring with symbol: {base_symbol}")
        
        # Verify the DETECTED symbol for MT5
        if not self.verify_symbol(detected_symbol):
            raise Exception(f"❌ Symbol {detected_symbol} not found")
    
        # Get pyramid structure from style
        pyramid_style = settings.get('pyramid_style', 'daily')
        if pyramid_style not in config.PYRAMID_STYLES:
            pyramid_style = 'daily'  # Fallback to daily
        
        pyramid_name, pyramid_structure = config.PYRAMID_STYLES[pyramid_style]
    
        # Set timeframe mappings for pyramid
        self.timeframes = {}
        for tf in pyramid_structure:
            self.timeframes[tf] = getattr(mt5, f"TIMEFRAME_{tf}")
    
        self.utc_offset = settings.get('utc_offset', 0)
    
        print(f"✅ Auto-configured: {self.symbol}, {pyramid_name}")
        return pyramid_structure, pyramid_name

    # ===========================================================
    # 📊 DATA FETCHING - UNIVERSAL SYMBOL SUPPORT
    # ===========================================================
    def fetch_timeframe_data(self, symbol: str, timeframe: str) -> Optional[pd.DataFrame]:
        """Fetch 200 candles for timeframe using the symbol parameter"""
        if not self.connected:
            print("❌ MT5 not connected")
            return None

        mt5_tf = getattr(mt5, f"TIMEFRAME_{timeframe}", None)
        if not mt5_tf:
            print(f"❌ Invalid timeframe: {timeframe}")
            return None

        # Use detected symbol for MT5 API calls
        actual_symbol = self.detect_symbol_suffix(symbol)
        print(f"📥 Fetching {actual_symbol} {timeframe} (200 candles)...")

        rates = mt5.copy_rates_from_pos(actual_symbol, mt5_tf, 0, 200)
        if rates is None or len(rates) == 0:
            print(f"⚠️ Primary method failed, trying fallback for {actual_symbol}/{timeframe}")
            current_time = datetime.now()
            rates = mt5.copy_rates_from(actual_symbol, mt5_tf, current_time, 200)

        if rates is None or len(rates) == 0:
            print(f"❌ Failed to fetch data for {actual_symbol}/{timeframe}")
            return None

        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit='s') + timedelta(hours=self.utc_offset)
        df = df.sort_values("time", ascending=False).reset_index(drop=True)
        print(f"✅ Fetched {len(df)} candles for {timeframe}")
        return df

    def fetch_unified_data(self, symbol: str, pyramid_structure: List[str]) -> Dict[str, pd.DataFrame]:
        """Fetch 200 candles for all timeframes in pyramid structure using symbol parameter"""
        data = {}
        for tf_name in pyramid_structure:
            df = self.fetch_timeframe_data(symbol, tf_name)
            data[tf_name] = df if df is not None else pd.DataFrame()
        return data

    def fetch_all_timeframes(self, symbol: str) -> Dict[str, pd.DataFrame]:
        """Fetch 200 candles for all timeframes using symbol parameter"""
        data = {}
        for tf_name in config.ALL_TIMEFRAMES:
            df = self.fetch_timeframe_data(symbol, tf_name)
            data[tf_name] = df if df is not None else pd.DataFrame()
        print(f"📊 Fetched all timeframes for {symbol}")
        return data

    # ===========================================================
    # 📈 REAL-TIME DATA
    # ===========================================================
    def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current bid price for any symbol"""
        if not self.connected:
            return None
        # Use detected symbol for MT5 call
        actual_symbol = self.detect_symbol_suffix(symbol)
        tick = mt5.symbol_info_tick(actual_symbol)
        return tick.bid if tick else None

    def get_symbol_info(self, symbol: str) -> Optional[Dict]:
        """Get comprehensive symbol info for any symbol"""
        if not self.connected:
            return None
        # Use detected symbol for MT5 call
        actual_symbol = self.detect_symbol_suffix(symbol)
        info = mt5.symbol_info(actual_symbol)
        if info:
            return {
                'name': info.name,
                'bid': info.bid,
                'ask': info.ask,
                'spread': info.spread,
                'digits': info.digits,
                'trade_mode': info.trade_mode
            }
        return None

    # ===========================================================
    # ❤️ HEALTH MONITORING
    # ===========================================================
    def health_check(self) -> Dict:
        """Return connector health status"""
        return {
            'connected': self.connected,
            'symbols_loaded': len(self.available_symbols),
            'current_symbol': self.symbol,
            'last_check': datetime.now().isoformat()
        }

# Singleton instance
mt5_connector = MT5Connector()