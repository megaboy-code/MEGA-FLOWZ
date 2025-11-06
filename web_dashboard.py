# ===============================================================
# WEB DASHBOARD - FLASK SERVER & API INTERFACE - DYNAMIC PERIODS
# ===============================================================
from flask import Flask, jsonify, render_template, send_from_directory, request
import threading
import webbrowser
import time
import os
from typing import Dict, Any
import config
import pandas as pd

class WebDashboard:
    def __init__(self):
        # Flask app configuration
        self.app = None
        self.dashboard_port = config.DEFAULT_SETTINGS['dashboard_port']
        self.setup_done = False
     
        # External module references (will be injected)
        self.mt5_connector = None
        self.pyramid_engine = None
        self.main_launcher = None  # ADDED: Reference to main launcher
     
        print("Web Dashboard initialized")

    # ===========================================================
    # MODULE INJECTION
    # ===========================================================
    def inject_modules(self, mt5_connector, pyramid_engine, main_launcher=None):  # MODIFIED: Added main_launcher
        """Inject required modules for operation"""
        self.mt5_connector = mt5_connector
        self.pyramid_engine = pyramid_engine
        self.main_launcher = main_launcher  # ADDED: Store main_launcher reference
        print("Modules injected into Web Dashboard")

    # ===========================================================
    # FLASK APP SETUP & ROUTES - FIXED: SYMBOL SWITCHING SUPPORT
    # ===========================================================
    def setup_flask_app(self):
        """Setup Flask application with all routes"""
        if self.setup_done:
            return
         
        self.app = Flask(__name__, template_folder="dashboard", static_folder="dashboard")
        self._setup_routes()
        self._create_dashboard_structure()
        self.setup_done = True
        print("Flask app setup complete")

    def _setup_routes(self):
        """Define all Flask API routes - FIXED: Symbol switching support"""
     
        # ==================== MAIN ROUTES ====================
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/<path:filename>')
        def serve_static(filename):
            return send_from_directory('dashboard', filename)

        # ==================== API ROUTES - FIXED: SYMBOL SWITCHING ====================
        @self.app.route('/api/pyramid')
        def api_pyramid():
            """Get current pyramid data - FIXED: Uses pyramid engine cache"""
            try:
                # Get current user settings from request
                pair = request.args.get('pair', 'EUR/USD').replace('/', '')
                pyramid_style = request.args.get('pyramid_style', 'daily')
                
                # FIXED: Use multi-symbol cache instead of waiting for MT5
                cached_pyramid = self.pyramid_engine.get_pyramid_for_symbol(pair)
                
                # Return cached pyramid data immediately
                return jsonify(cached_pyramid)
                
            except Exception as e:
                return jsonify({"error": f"Pyramid API error: {str(e)}"}), 500

        @self.app.route('/api/chart-data/<timeframe>')
        def api_chart_data(timeframe):
            """Get chart data for specific timeframe - FIXED: Uses pyramid engine cache"""
            try:
                # Get current user settings
                pair = request.args.get('pair', 'EUR/USD').replace('/', '')
                
                # FIXED: Use cached data from pyramid engine multi-symbol cache
                cached_raw_data = self.pyramid_engine.get_raw_data_for_symbol(pair)
                
                if not cached_raw_data:
                    return jsonify({"error": "No chart data available yet - please wait for initial load"}), 404
             
                if timeframe not in cached_raw_data:
                    return jsonify({"error": f"Timeframe {timeframe} not available in cached data"}), 404
                
                # FIXED: Extract user periods from request
                custom_periods = self._extract_custom_periods(request)
             
                chart_data = self.pyramid_engine.get_chart_data(
                    cached_raw_data,
                    timeframe
                )
             
                # FIXED: Calculate indicators with DYNAMIC periods
                df_with_indicators = self.pyramid_engine.calculate_technical_indicators(
                    cached_raw_data[timeframe].copy(),
                    custom_periods
                )

                # FIXED: Get REAL indicator values with dynamic periods
                real_indicator_values = self.pyramid_engine.get_current_indicator_values(df_with_indicators)
                
                # FIXED: Format indicator data for chart with dynamic periods
                indicators_data = self.pyramid_engine.get_indicator_chart_data(df_with_indicators, timeframe)

                return jsonify({
                    "symbol": pair,
                    "timeframe": timeframe,
                    "data": chart_data,
                    "total_candles": len(chart_data),
                    "indicators": real_indicator_values,  # FIXED: Dynamic period values
                    "indicators_data": indicators_data    # FIXED: Dynamic period chart data
                })
             
            except Exception as e:
                return jsonify({"error": f"Chart error: {str(e)}"}), 500

        @self.app.route('/api/analysis')
        def api_analysis():
            """Get technical analysis and signals"""
            try:
                # FIXED: Use current symbol's cached pyramid
                current_symbol = self.mt5_connector.symbol if self.mt5_connector else 'EURUSD'
                cached_pyramid = self.pyramid_engine.get_pyramid_for_symbol(current_symbol)
                
                if not cached_pyramid or not cached_pyramid.get('blocks'):
                    return jsonify({"error": "No pyramid data available"})
             
                analysis = {
                    "technical_summary": self.pyramid_engine.generate_technical_summary(),
                    "trading_signals": self.pyramid_engine.generate_trading_signals(),
                    "market_structure": self.pyramid_engine.analyze_market_structure()
                }
                return jsonify(analysis)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route('/api/alerts')
        def api_alerts():
            """Get alert settings and active alerts"""
            return jsonify({
                "active_alerts": [],
                "settings": {
                    "rsi_alerts": True,
                    "price_alerts": False,
                    "volume_alerts": True
                }
            })

        @self.app.route('/api/health')
        def api_health():
            """Health check endpoint"""
            mt5_health = self.mt5_connector.health_check() if self.mt5_connector else {}
            return jsonify({
                "status": "healthy",
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                "symbol": self.mt5_connector.symbol if self.mt5_connector else "Unknown",
                "pyramid_structure": self.pyramid_engine.pyramid_structure if self.pyramid_engine else [],
                "cached_symbols": self.pyramid_engine.get_cached_symbols() if self.pyramid_engine else [],  # NEW: Show cached symbols
                "mt5": mt5_health
            })

        # ==================== UPDATE SETTINGS ROUTE - FIXED: SYMBOL SWITCHING ====================
        @self.app.route('/api/update-settings', methods=['POST'])
        def api_update_settings():
            """Update system settings from frontend - FIXED: No cache clearing"""
            try:
                settings = request.json
                if not settings:
                    return jsonify({"error": "No settings provided"}), 400
                
                print(f"🔄 Processing symbol change to: {settings.get('symbol')}")
                
                # ❌ REMOVED: Cache clearing - keep cache intact!
                # self.pyramid_engine.latest_raw_data.clear()
                # self.pyramid_engine.latest_pyramid.clear()
                print("✅ Cache preserved for symbol switch")
                
                # Update MT5 connector with new settings
                pyramid_structure, pyramid_name = self.mt5_connector.configure_from_settings(settings)
                
                # Update pyramid engine configuration
                self.pyramid_engine.configure_pyramid(
                    symbol=settings.get('symbol', 'EURUSD'),
                    pyramid_structure=pyramid_structure,
                    pyramid_style=settings.get('pyramid_style', 'daily'),
                    utc_offset=settings.get('utc_offset', 0)
                )
                
                # FIXED: Update main_launcher symbol if available
                if self.main_launcher:
                    self.main_launcher.symbol = self.mt5_connector.symbol
                    print(f"🔄 Main launcher symbol updated to: {self.main_launcher.symbol}")
                
                # FIXED: Trigger immediate data fetch for new symbol
                try:
                    print(f"🚀 Immediate fetch triggered for: {self.mt5_connector.symbol}")
                    raw_data = self.mt5_connector.fetch_all_timeframes(self.mt5_connector.symbol)
                    
                    if raw_data:
                        # Process data through pyramid engine
                        pyramid_data = {}
                        for tf in raw_data:
                            if not raw_data[tf].empty:
                                pyramid_data[tf] = self.pyramid_engine.calculate_momentum_analysis(raw_data[tf])
                        
                        # Build pyramid JSON
                        pyramid_json = self.pyramid_engine.build_pyramid_json(pyramid_data)
                        
                        # Save to storage
                        self.pyramid_engine.save_to_json(pyramid_json)
                        
                        # FIXED: Update multi-symbol cache with new data
                        self.pyramid_engine.update_symbol_data(
                            self.mt5_connector.symbol, 
                            raw_data, 
                            pyramid_json
                        )
                        
                        print(f"✅ Immediate fetch completed: {len(pyramid_json.get('blocks', []))} blocks, {len(raw_data)} TFs")
                    else:
                        print("❌ Immediate fetch failed - no data returned")
                        
                except Exception as fetch_error:
                    print(f"⚠️ Immediate fetch failed: {fetch_error}")
                    return jsonify({"error": f"Fetch failed: {str(fetch_error)}"}), 500
                
                return jsonify({
                    "status": "success",
                    "message": f"Settings updated: {settings.get('symbol')}, {settings.get('pyramid_style')}",
                    "pyramid_structure": pyramid_structure
                })
                
            except Exception as e:
                return jsonify({"error": f"Settings update failed: {str(e)}"}), 500

    # ==================== FIXED: DYNAMIC PERIODS EXTRACTION ====================
    def _extract_custom_periods(self, request):
        """Extract custom indicator periods from request parameters"""
        custom_periods = {}
        
        # Extract all period parameters from request
        for key, value in request.args.items():
            if key.endswith('_period'):
                try:
                    period_value = int(value)
                    custom_periods[key] = period_value
                except (ValueError, TypeError):
                    continue
                    
            # Handle multiple instances (sma_period_1, sma_period_2, etc.)
            elif '_period_' in key:
                try:
                    period_value = int(value)
                    custom_periods[key] = period_value
                except (ValueError, TypeError):
                    continue
        
        return custom_periods

    # ===========================================================
    # DASHBOARD FILE STRUCTURE
    # ===========================================================
    def _create_dashboard_structure(self):
        """Create dashboard directory structure"""
        dashboard_path = "dashboard"
     
        # Create dashboard directory
        if os.path.exists(dashboard_path):
            if os.path.isfile(dashboard_path):
                print(f"Conflict: '{dashboard_path}' is a FILE. Deleting it...")
                os.remove(dashboard_path)
        os.makedirs(dashboard_path, exist_ok=True)
        # Create empty data.json file
        self._create_data_json()
        print("Dashboard structure created")

    def _create_data_json(self):
        """Create initial data.json file for dashboard"""
        initial_data = {
            "symbol": "Loading...",
            "style": "Loading...",
            "structure": [],
            "generated": time.strftime('%Y-%m-%dT%H:%M:%S'),
            "blocks": []
        }
     
        data_path = os.path.join("dashboard", "data.json")
        import json
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(initial_data, f, indent=2)

    # ===========================================================
    # SERVER CONTROL
    # ===========================================================
    def start_flask_server(self):
        """Start Flask server in a separate thread"""
        def run_flask():
            print(f"Starting Flask server on port {self.dashboard_port}...")
            self.app.run(
                host='127.0.0.1',
                port=self.dashboard_port,
                use_reloader=False,
                debug=False
            )
     
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        print(f"Flask server thread started")

    def open_browser(self):
        """Open web browser to dashboard"""
        time.sleep(3) # Give server time to start
        url = f"http://127.0.0.1:{self.dashboard_port}"
        webbrowser.open(url)
        print(f"Dashboard opened: {url}")

    # ===========================================================
    # DASHBOARD OPERATIONS - FIXED: SYMBOL SWITCHING SUPPORT
    # ===========================================================
    def update_dashboard_data(self, raw_data: Dict, pyramid_data: Dict):
        """Update dashboard with new data - FIXED: Updates multi-symbol cache"""
        try:
            # FIXED: Update multi-symbol cache instead of just single-symbol state
            symbol = pyramid_data.get('symbol', self.mt5_connector.symbol if self.mt5_connector else 'Unknown')
            self.pyramid_engine.update_symbol_data(symbol, raw_data, pyramid_data)
         
            # Save to JSON for persistence
            self.pyramid_engine.save_to_json(pyramid_data)
         
            print(f"Dashboard updated: {len(pyramid_data.get('blocks', []))} blocks for {symbol}")
            return True
         
        except Exception as e:
            print(f"Dashboard update error: {e}")
            return False

    def get_dashboard_status(self) -> Dict[str, Any]:
        """Get current dashboard status"""
        return {
            'server_running': self.setup_done,
            'port': self.dashboard_port,
            'symbol': self.mt5_connector.symbol if self.mt5_connector else None,
            'pyramid_style': self.pyramid_engine.pyramid_style if self.pyramid_engine else None,
            'cached_symbols': self.pyramid_engine.get_cached_symbols() if self.pyramid_engine else [],  # NEW: Show cached symbols
            'last_update': time.strftime('%Y-%m-%d %H:%M:%S')
        }

    def cleanup(self):
        """Cleanup dashboard resources"""
        print("Cleaning up dashboard resources...")

# Singleton instance
web_dashboard = WebDashboard()