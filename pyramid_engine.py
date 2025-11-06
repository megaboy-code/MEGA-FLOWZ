# ===============================================================
# 🏗️ PYRAMID ENGINE - ENHANCED WITH MULTI-SYMBOL CACHE
# ===============================================================

import pandas as pd
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Any, Optional
import config

class PyramidEngine:
    def __init__(self):
        # Pyramid configuration
        self.symbol = None
        self.pyramid_style = None
        self.pyramid_structure = []
        self.base_tf = None
        self.extract_count = config.DEFAULT_SETTINGS['extract_count']
        self.utc_offset = 0
        
        # Multi-symbol cache - NEW
        self.pyramid_cache = {}      # symbol -> pyramid_data
        self.raw_data_cache = {}     # symbol -> raw_data
        self.current_symbol = None
        
        # Legacy single-symbol state (for backward compatibility)
        self.latest_pyramid = {}
        self.latest_raw_data = {}
        self.json_filename = "latest_pyramid.json"
        
        print("🏗️ Pyramid Engine initialized with multi-symbol cache")

    # ===========================================================
    # 🎯 CONFIGURATION SETUP
    # ===========================================================
    def configure_pyramid(self, symbol: str, pyramid_structure: List[str], pyramid_style: str, utc_offset: int):
        """Configure pyramid parameters"""
        self.symbol = symbol
        self.pyramid_structure = pyramid_structure
        self.pyramid_style = pyramid_style
        self.base_tf = pyramid_structure[0]
        self.utc_offset = utc_offset
        self.current_symbol = symbol
        print(f"✅ Pyramid configured: {symbol}, {pyramid_style}")

    # ===========================================================
    # 🔄 MULTI-SYMBOL CACHE MANAGEMENT - NEW
    # ===========================================================
    def get_pyramid_for_symbol(self, symbol: str) -> Dict[str, Any]:
        """Get cached pyramid for specific symbol - lazy initialization"""
        if symbol in self.pyramid_cache:
            return self.pyramid_cache[symbol]
        else:
            # Lazy initialization - create empty pyramid for new symbol
            print(f"🆕 First request for {symbol}, creating empty pyramid cache")
            empty_pyramid = self._create_empty_pyramid()
            empty_pyramid['symbol'] = symbol
            self.pyramid_cache[symbol] = empty_pyramid
            return empty_pyramid

    def get_raw_data_for_symbol(self, symbol: str) -> Dict[str, pd.DataFrame]:
        """Get cached raw data for specific symbol"""
        if symbol in self.raw_data_cache:
            return self.raw_data_cache[symbol]
        else:
            # Create empty raw data structure
            empty_data = {tf: pd.DataFrame() for tf in config.ALL_TIMEFRAMES}
            self.raw_data_cache[symbol] = empty_data
            return empty_data

    def update_symbol_data(self, symbol: str, raw_data: Dict[str, pd.DataFrame], pyramid_data: Dict[str, Any]):
        """Update cache for specific symbol"""
        # Update multi-symbol cache
        self.pyramid_cache[symbol] = pyramid_data
        self.raw_data_cache[symbol] = raw_data
        
        # Update current symbol for backward compatibility
        if symbol == self.current_symbol:
            self.latest_pyramid = pyramid_data
            self.latest_raw_data = raw_data
            
        print(f"💾 Updated cache for {symbol}: {len(pyramid_data.get('blocks', []))} blocks")

    def clear_symbol_cache(self, symbol: str):
        """Clear cache for specific symbol"""
        if symbol in self.pyramid_cache:
            del self.pyramid_cache[symbol]
        if symbol in self.raw_data_cache:
            del self.raw_data_cache[symbol]
        print(f"🧹 Cleared cache for {symbol}")

    def get_cached_symbols(self) -> List[str]:
        """Get list of all symbols with cached data"""
        return list(self.pyramid_cache.keys())

    # ===========================================================
    # 📊 MOMENTUM & CANDLE ANALYSIS CALCULATIONS
    # ===========================================================
    def calculate_momentum_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate momentum indicators and candle analysis"""
        # Simple direction based on close vs open
        df["Momentum"] = df["close"] - df["open"]
        df["Dir"] = df["Momentum"].apply(lambda x: "🟢" if x > 0 else "🔴" if x < 0 else "⚪")
        
        # Momentum Acceleration
        df["Momentum_Acceleration"] = (df["close"] - df["close"].shift(1)) - (df["close"].shift(1) - df["close"].shift(2))
        
        # Wick Ratio (upper wick vs lower wick)
        denominator = df["close"] - df["low"]
        denominator = denominator.replace(0, 0.00001)  # Avoid division by zero
        df["Wick_Ratio"] = (df["high"] - df["close"]) / denominator
        df["Wick_Ratio"] = df["Wick_Ratio"].abs()
        
        # Body Strength (body size relative to total range)
        range_denominator = df["high"] - df["low"]
        range_denominator = range_denominator.replace(0, 0.00001)
        df["Body_Strength"] = (df["close"] - df["open"]).abs() / range_denominator
        
        # ATR Calculation (14-period)
        hl = df['high'] - df['low']
        hc = (df['high'] - df['close'].shift()).abs()
        lc = (df['low'] - df['close'].shift()).abs()
        tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)
        df["ATR"] = tr.rolling(14, min_periods=1).mean()
        
        return df

    def get_momentum_summary(self, df: pd.DataFrame, index: int = 0) -> str:
        """Generate momentum summary text for a candle"""
        row = df.iloc[index]
        
        mom_accel = row.get("Momentum_Acceleration", 0)
        mom_text = f"MOM: {mom_accel:+.5f}" if not pd.isna(mom_accel) else "MOM: --"
        
        wick_ratio = row.get("Wick_Ratio", 0)
        wick_text = f"WICK: {wick_ratio:.2f}x" if not pd.isna(wick_ratio) else "WICK: --"
        
        body_strength = row.get("Body_Strength", 0)
        body_text = f"BODY: {body_strength:.0%}" if not pd.isna(body_strength) else "BODY: --"
        
        atr = row.get("ATR", 0)
        atr_text = f"ATR: {atr:.5f}" if not pd.isna(atr) else "ATR: --"
        
        return f"{mom_text} | {wick_text} | {body_text} | {atr_text}"

    # ===========================================================
    # 🕒 TIME RANGE FORMATTING
    # ===========================================================
    def get_time_range(self, t: datetime, tf: str) -> str:
        """Format time range for display based on timeframe"""
        fmt = config.CHART_CONFIG['time_range_formats'].get(tf, "%H:%M")
        start = t.strftime(fmt)
        
        if tf == "D1": 
            return f"[{start}]"
            
        end_min = {"M1": 0, "M5": 4, "M15": 14, "H1": 59, "H4": 239}.get(tf, 0)
        end = (t + timedelta(minutes=end_min)).strftime("%H:%M")
        return f"[{start}-{end}]" if tf != "M1" else f"[{start}]"

    # ===========================================================
    # 🧩 PYRAMID JSON CONSTRUCTION - ENHANCED WITH VOLUME
    # ===========================================================
    def build_pyramid_json(self, data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Build complete pyramid JSON structure with volume"""
        if self.base_tf not in data or data[self.base_tf].empty:
            return self._create_empty_pyramid()
            
        base_df = data[self.base_tf].iloc[:self.extract_count]
        blocks = []

        def get_children(parent_time: datetime, parent_tf: str, level: int = 0) -> List[Dict]:
            """Recursively get child blocks for parent timeframe"""
            if level + 1 >= len(self.pyramid_structure): 
                return []
                
            child_tf = self.pyramid_structure[level + 1]
            if child_tf not in data or data[child_tf].empty:
                return []
                
            df = data[child_tf]
            start = parent_time
            end = parent_time + timedelta(minutes=config.TIMEFRAME_DURATIONS[parent_tf])
            
            # Filter children within parent time range
            children_df = df[(df["time"] >= start) & (df["time"] < end)]
            children = []
            
            for _, row in children_df.iterrows():
                child_index = df[df["time"] == row["time"]].index[0]
                child = {
                    "tf": child_tf,
                    "time": row["time"].isoformat(),
                    "range": self.get_time_range(row["time"], child_tf),
                    "O": round(row["open"], 5),
                    "H": round(row["high"], 5),
                    "L": round(row["low"], 5),
                    "C": round(row["close"], 5),
                    "volume": int(row.get("tick_volume", 0)),  # ADDED: Volume data
                    "dir": row["Dir"],
                    "momentum_summary": self.get_momentum_summary(df, child_index),
                    "children": get_children(row["time"], child_tf, level + 1)
                }
                children.append(child)
            return children

        # Build base blocks with volume
        for _, row in base_df.iterrows():
            block_index = base_df[base_df["time"] == row["time"]].index[0]
            block = {
                "tf": self.base_tf,
                "time": row["time"].isoformat(),
                "range": self.get_time_range(row["time"], self.base_tf),
                "O": round(row["open"], 5),
                "H": round(row["high"], 5),
                "L": round(row["low"], 5),
                "C": round(row["close"], 5),
                "volume": int(row.get("tick_volume", 0)),  # ADDED: Volume data
                "dir": row["Dir"],
                "momentum_summary": self.get_momentum_summary(base_df, block_index),
                "children": get_children(row["time"], self.base_tf)
            }
            blocks.append(block)

        pyramid = {
            "symbol": self.symbol,
            "style": self.pyramid_style,
            "structure": self.pyramid_structure,
            "generated": datetime.now().isoformat(),
            "blocks": blocks
        }
        
        return pyramid

    def _create_empty_pyramid(self) -> Dict[str, Any]:
        """Create empty pyramid structure when no data available"""
        return {
            "symbol": self.symbol or "Unknown",
            "style": self.pyramid_style or "Unknown",
            "structure": self.pyramid_structure,
            "generated": datetime.now().isoformat(),
            "blocks": []
        }

    # ===========================================================
    # 📈 TECHNICAL INDICATORS CALCULATION - ENHANCED
    # ===========================================================
    def calculate_technical_indicators(self, df: pd.DataFrame, custom_periods: Optional[Dict] = None) -> pd.DataFrame:
        """Calculate technical indicators with DYNAMIC user periods"""
        try:
            # Ensure we have enough data for calculations
            if len(df) < 20:
                return df
            
            # Use custom periods if provided, otherwise use defaults
            periods = self._get_periods(custom_periods)
                
            # SMA - Dynamic periods
            for sma_period in periods['sma_periods']:
                col_name = f'SMA_{sma_period}'
                df[col_name] = df['close'].rolling(window=min(sma_period, len(df)), min_periods=1).mean()
            
            # EMA - Dynamic periods  
            for ema_period in periods['ema_periods']:
                col_name = f'EMA_{ema_period}'
                df[col_name] = df['close'].ewm(span=min(ema_period, len(df)), adjust=False).mean()
            
            # MACD - Dynamic periods
            macd_fast = periods['macd_fast']
            macd_slow = periods['macd_slow']
            macd_signal = periods['macd_signal']
            
            ema_fast = df['close'].ewm(span=min(macd_fast, len(df)), adjust=False).mean()
            ema_slow = df['close'].ewm(span=min(macd_slow, len(df)), adjust=False).mean()
            df['MACD'] = ema_fast - ema_slow
            df['MACD_Signal'] = df['MACD'].ewm(span=min(macd_signal, len(df)), adjust=False).mean()
            df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
            
            # RSI - Dynamic period
            rsi_period = periods['rsi_period']
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=min(rsi_period, len(df)), min_periods=1).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=min(rsi_period, len(df)), min_periods=1).mean()
            
            # Avoid division by zero
            rs = gain / loss.replace(0, 0.00001)
            df['RSI'] = 100 - (100 / (1 + rs))
            
            # Bollinger Bands - Dynamic period
            bb_period = periods['bb_period']
            df['BB_Middle'] = df['close'].rolling(window=min(bb_period, len(df)), min_periods=1).mean()
            bb_std = df['close'].rolling(window=min(bb_period, len(df)), min_periods=1).std()
            df['BB_Upper'] = df['BB_Middle'] + (bb_std.fillna(0) * 2)
            df['BB_Lower'] = df['BB_Middle'] - (bb_std.fillna(0) * 2)
            
            # ADDED: Stochastic Oscillator
            stoch_k = periods.get('stoch_k', 14)
            stoch_d = periods.get('stoch_d', 3)
            
            # %K Line
            low_min = df['low'].rolling(window=min(stoch_k, len(df)), min_periods=1).min()
            high_max = df['high'].rolling(window=min(stoch_k, len(df)), min_periods=1).max()
            df['Stoch_%K'] = 100 * ((df['close'] - low_min) / (high_max - low_min).replace(0, 0.00001))
            
            # %D Line (signal)
            df['Stoch_%D'] = df['Stoch_%K'].rolling(window=min(stoch_d, len(df)), min_periods=1).mean()
            
            # ADDED: Support/Resistance Levels
            sr_levels = self.calculate_support_resistance(df)
            df['Support_Levels'] = [sr_levels['support']] * len(df)
            df['Resistance_Levels'] = [sr_levels['resistance']] * len(df)
            
            # Fill NaN values
            self._fill_indicator_nans(df)
            
        except Exception as e:
            print(f"⚠️ Indicator calculation warning: {e}")
        
        return df

    def _get_periods(self, custom_periods: Optional[Dict] = None) -> Dict:
        """Get indicator periods - custom if provided, otherwise defaults"""
        if not custom_periods:
            return {
                'sma_periods': [20, 50],
                'ema_periods': [12, 26],
                'macd_fast': 12,
                'macd_slow': 26, 
                'macd_signal': 9,
                'rsi_period': 14,
                'bb_period': 20,
                'stoch_k': 14,
                'stoch_d': 3
            }
        
        # Extract custom periods from request
        periods = {
            'sma_periods': [],
            'ema_periods': [],
            'macd_fast': custom_periods.get('macd_fast', 12),
            'macd_slow': custom_periods.get('macd_slow', 26),
            'macd_signal': custom_periods.get('macd_signal', 9),
            'rsi_period': custom_periods.get('rsi_period', 14),
            'bb_period': custom_periods.get('bb_period', 20),
            'stoch_k': custom_periods.get('stoch_k', 14),
            'stoch_d': custom_periods.get('stoch_d', 3)
        }
        
        # Handle multiple SMA/EMA instances
        sma_periods = [v for k, v in custom_periods.items() if k.startswith('sma_period')]
        ema_periods = [v for k, v in custom_periods.items() if k.startswith('ema_period')]
        
        # Use custom periods or defaults
        periods['sma_periods'] = sma_periods if sma_periods else [20, 50]
        periods['ema_periods'] = ema_periods if ema_periods else [12, 26]
        
        return periods

    def _fill_indicator_nans(self, df: pd.DataFrame):
        """Fill NaN values in indicator columns"""
        indicator_columns = [col for col in df.columns if any(indicator in col for indicator in 
                            ['SMA_', 'EMA_', 'MACD', 'RSI', 'BB_', 'Stoch_'])]
        
        for col in indicator_columns:
            if col in df.columns:
                df[col] = df[col].ffill().bfill()

    def get_current_indicator_values(self, df: pd.DataFrame) -> Dict[str, float]:
        """Get current/latest values for all calculated indicators"""
        if df.empty:
            return {}
            
        latest = df.iloc[-1]
        values = {}
        
        # Extract all indicator values from the latest row
        for col in df.columns:
            if any(indicator in col for indicator in ['SMA_', 'EMA_', 'MACD', 'RSI', 'BB_', 'Stoch_']):
                if not pd.isna(latest[col]):
                    values[col.lower()] = float(latest[col])
        
        return values

    def get_indicator_chart_data(self, df: pd.DataFrame, timeframe: str) -> Dict[str, Any]:
        """Format indicator data for chart.js plotting with ENHANCED structure"""
        indicators_data = {}
        
        if df.empty:
            return indicators_data
            
        time_data = df['time'].tolist()
        
        # Format all SMA lines
        sma_columns = [col for col in df.columns if col.startswith('SMA_')]
        for col in sma_columns:
            period = col.replace('SMA_', '')
            indicators_data[f'sma_{period}'] = [
                {'x': time_data[i].timestamp() * 1000, 'y': float(df[col].iloc[i])} 
                for i in range(len(df)) if not pd.isna(df[col].iloc[i])
            ]
        
        # Format all EMA lines  
        ema_columns = [col for col in df.columns if col.startswith('EMA_')]
        for col in ema_columns:
            period = col.replace('EMA_', '')
            indicators_data[f'ema_{period}'] = [
                {'x': time_data[i].timestamp() * 1000, 'y': float(df[col].iloc[i])}
                for i in range(len(df)) if not pd.isna(df[col].iloc[i])
            ]
        
        # Format RSI
        if 'RSI' in df.columns:
            indicators_data['rsi'] = [
                {'x': time_data[i].timestamp() * 1000, 'y': float(df['RSI'].iloc[i])}
                for i in range(len(df)) if not pd.isna(df['RSI'].iloc[i])
            ]
        
        # Format MACD
        if 'MACD' in df.columns:
            indicators_data['macd'] = [
                {'x': time_data[i].timestamp() * 1000, 'y': float(df['MACD'].iloc[i])}
                for i in range(len(df)) if not pd.isna(df['MACD'].iloc[i])
            ]
            
        if 'MACD_Signal' in df.columns:
            indicators_data['macd_signal'] = [
                {'x': time_data[i].timestamp() * 1000, 'y': float(df['MACD_Signal'].iloc[i])}
                for i in range(len(df)) if not pd.isna(df['MACD_Signal'].iloc[i])
            ]
        
        # ENHANCED: Format Bollinger Bands as grouped object
        if all(col in df.columns for col in ['BB_Upper', 'BB_Middle', 'BB_Lower']):
            indicators_data['bollinger'] = {
                'upper': [
                    {'x': time_data[i].timestamp() * 1000, 'y': float(df['BB_Upper'].iloc[i])}
                    for i in range(len(df)) if not pd.isna(df['BB_Upper'].iloc[i])
                ],
                'middle': [
                    {'x': time_data[i].timestamp() * 1000, 'y': float(df['BB_Middle'].iloc[i])}
                    for i in range(len(df)) if not pd.isna(df['BB_Middle'].iloc[i])
                ],
                'lower': [
                    {'x': time_data[i].timestamp() * 1000, 'y': float(df['BB_Lower'].iloc[i])}
                    for i in range(len(df)) if not pd.isna(df['BB_Lower'].iloc[i])
                ]
            }
        
        # ADDED: Format Stochastic Oscillator
        if 'Stoch_%K' in df.columns:
            indicators_data['stoch_k'] = [
                {'x': time_data[i].timestamp() * 1000, 'y': float(df['Stoch_%K'].iloc[i])}
                for i in range(len(df)) if not pd.isna(df['Stoch_%K'].iloc[i])
            ]
            
        if 'Stoch_%D' in df.columns:
            indicators_data['stoch_d'] = [
                {'x': time_data[i].timestamp() * 1000, 'y': float(df['Stoch_%D'].iloc[i])}
                for i in range(len(df)) if not pd.isna(df['Stoch_%D'].iloc[i])
            ]
        
        # ADDED: Format Support/Resistance Levels
        if 'Support_Levels' in df.columns and 'Resistance_Levels' in df.columns:
            support_levels = df['Support_Levels'].iloc[0] if len(df) > 0 else []
            resistance_levels = df['Resistance_Levels'].iloc[0] if len(df) > 0 else []
            
            indicators_data['support_resistance'] = {
                'support': support_levels,
                'resistance': resistance_levels,
                'time_range': {
                    'start': time_data[0].timestamp() * 1000,
                    'end': time_data[-1].timestamp() * 1000
                }
            }
        
        return indicators_data

    # ADDED: Support/Resistance Calculation
    def calculate_support_resistance(self, df: pd.DataFrame, lookback: int = 20) -> Dict[str, List[float]]:
        """Calculate support and resistance levels from price action"""
        levels = {'support': [], 'resistance': []}
        
        if len(df) < lookback * 2:
            return levels
            
        for i in range(lookback, len(df) - lookback):
            # Swing High detection (Resistance)
            if all(df['high'].iloc[i] > df['high'].iloc[i-j] for j in range(1, lookback+1)) and \
               all(df['high'].iloc[i] > df['high'].iloc[i+j] for j in range(1, lookback+1)):
                level = float(df['high'].iloc[i])
                # Avoid duplicate levels (within 0.1% range)
                if not any(abs(level - existing) / existing < 0.001 for existing in levels['resistance']):
                    levels['resistance'].append(level)
            
            # Swing Low detection (Support)  
            if all(df['low'].iloc[i] < df['low'].iloc[i-j] for j in range(1, lookback+1)) and \
               all(df['low'].iloc[i] < df['low'].iloc[i+j] for j in range(1, lookback+1)):
                level = float(df['low'].iloc[i])
                # Avoid duplicate levels (within 0.1% range)
                if not any(abs(level - existing) / existing < 0.001 for existing in levels['support']):
                    levels['support'].append(level)
        
        # Sort and keep strongest levels (limit to 5 each)
        levels['support'] = sorted(levels['support'])[-5:]
        levels['resistance'] = sorted(levels['resistance'])[:5]
        
        return levels

    # ===========================================================
    # 📊 CHART DATA PREPARATION - FIXED VERSION
    # ===========================================================
    def get_chart_data(self, data: Dict[str, pd.DataFrame], timeframe: str) -> List[Dict]:
        """Extract chart data for line/area charts - FIXED with proper data structure"""
        if timeframe not in data or data[timeframe].empty:
            return []
            
        df = data[timeframe]
        chart_data = []
        
        for _, row in df.iterrows():
            chart_data.append({
                'x': row["time"].timestamp() * 1000,  # JavaScript timestamp
                'y': float(row["close"]),  # Use close price for line/area charts
                'o': float(row["open"]),
                'h': float(row["high"]),
                'l': float(row["low"]),
                'c': float(row["close"]),
                'volume': int(row.get("tick_volume", 0))
            })
        
        chart_data.reverse()  # Oldest first for charts
        return chart_data

    # ===========================================================
    # 💾 DATA PERSISTENCE
    # ===========================================================
    def save_to_json(self, pyramid_data: Dict[str, Any]):
        """Save pyramid data to JSON files"""
        # Update both single-symbol and multi-symbol cache
        symbol = pyramid_data.get('symbol', self.symbol)
        if symbol:
            self.pyramid_cache[symbol] = pyramid_data
            
        self.latest_pyramid = pyramid_data
        
        # Save to main JSON file
        with open(self.json_filename, "w", encoding="utf-8") as f:
            json.dump(pyramid_data, f, indent=2, ensure_ascii=False)
            
        # Save to dashboard data file
        dashboard_path = os.path.join("dashboard", "data.json")
        with open(dashboard_path, "w", encoding="utf-8") as f:
            json.dump(pyramid_data, f, indent=2, ensure_ascii=False)
            
        print(f"💾 Pyramid data saved: {len(pyramid_data.get('blocks', []))} blocks")

    # ===========================================================
    # 🧠 ANALYSIS & SIGNALS
    # ===========================================================
    def generate_technical_summary(self) -> str:
        """Generate technical summary from latest pyramid"""
        if not self.latest_pyramid or not self.latest_pyramid.get('blocks'):
            return "No data available for analysis"
        
        latest_block = self.latest_pyramid['blocks'][0]
        return f"Latest {latest_block['tf']} block: {latest_block['dir']} - {latest_block['momentum_summary']}"

    def generate_trading_signals(self) -> List[str]:
        """Generate trading signals from pyramid analysis"""
        signals = []
        if self.latest_pyramid and self.latest_pyramid.get('blocks'):
            latest = self.latest_pyramid['blocks'][0]
            if "Strong" in latest['momentum_summary'] and latest['dir'] == "🟢":
                signals.append("Potential BUY signal - Strong bullish momentum")
            elif "Strong" in latest['momentum_summary'] and latest['dir'] == "🔴":
                signals.append("Potential SELL signal - Strong bearish momentum")
        
        return signals if signals else ["No strong signals detected"]

    def analyze_market_structure(self) -> str:
        """Analyze overall market structure"""
        if not self.latest_pyramid or not self.latest_pyramid.get('blocks'):
            return "Waiting for market data..."
        
        structure = self.latest_pyramid['structure']
        return f"Monitoring {len(structure)} timeframes: {' → '.join(structure)}"

    # ===========================================================
    # 🔄 DATA STATE MANAGEMENT
    # ===========================================================
    def update_data_state(self, raw_data: Dict[str, pd.DataFrame], pyramid_data: Dict[str, Any]):
        """Update internal data state"""
        # Update both single-symbol and multi-symbol cache
        symbol = pyramid_data.get('symbol', self.symbol)
        if symbol:
            self.update_symbol_data(symbol, raw_data, pyramid_data)
        else:
            self.latest_raw_data = raw_data
            self.latest_pyramid = pyramid_data

    def get_current_data(self) -> Dict[str, Any]:
        """Get current data state"""
        return {
            'raw_data': self.latest_raw_data,
            'pyramid': self.latest_pyramid,
            'symbol': self.symbol,
            'structure': self.pyramid_structure,
            'cached_symbols': self.get_cached_symbols()  # NEW: Show cached symbols
        }

# Singleton instance
pyramid_engine = PyramidEngine()