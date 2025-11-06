# ===============================================================
# 🎯 MAIN LAUNCHER - SYSTEM ORCHESTRATION & CONTROL - FIXED VERSION
# ===============================================================

import time
import threading
import atexit
from datetime import datetime
import signal
import sys
from typing import Dict, Any

# Import our modules
import config
from mt5_connector import mt5_connector
from pyramid_engine import pyramid_engine
from web_dashboard import web_dashboard
from storage_manager import storage_layer  # ← ADDED STORAGE

class MainLauncher:
    def __init__(self):
        # System state
        self.running = False
        self.stop_event = threading.Event()
        
        # Configuration
        self.fetch_interval = config.DEFAULT_SETTINGS['fetch_interval']
        self.symbol = None
        self.pyramid_structure = []
        self.pyramid_style = None
        
        # Threading
        self.collector_thread = None
        
        print("🎯 Main Launcher initialized")

    # ===========================================================
    # 🚀 SYSTEM INITIALIZATION
    # ===========================================================
    def initialize_system(self) -> bool:
        """Initialize all system components"""
        try:
            print("🚀 Starting MEGA FLOWZ System...")
            print("======================================")
            
            # Phase 1: Initialize MT5 Connection
            print("\n📋 PHASE 1: Initializing core services...")
            if not self._initialize_mt5():
                return False
            print("   ✅ MT5 Connector ready")
            
            # Phase 2: Load configuration from STORAGE
            print("\n⚙️ PHASE 2: Loading configuration...")
            if not self._load_configuration():
                return False
            print("   ✅ Configuration loaded")
                
            # Phase 3: Initialize Pyramid Engine
            print("\n🏗️ PHASE 3: Initializing pyramid engine...")
            self._initialize_pyramid_engine()
            print("   ✅ Pyramid Engine ready")
            
            # Phase 4: Initialize Web Dashboard
            print("\n🌐 PHASE 4: Initializing web interface...")
            self._initialize_web_dashboard()
            print("   ✅ Web Dashboard ready")
            
            # Phase 5: Load initial data
            print("\n📥 PHASE 5: Loading initial market data...")
            if not self._load_initial_data():
                print("⚠️  Initial data loading had issues, but continuing...")
                
            print("\n✅ System initialization complete!")
            return True
            
        except Exception as e:
            print(f"❌ System initialization failed: {e}")
            return False

    def _initialize_mt5(self) -> bool:
        """Initialize MT5 connection"""
        try:
            return mt5_connector.initialize_mt5()
        except Exception as e:
            print(f"❌ MT5 initialization failed: {e}")
            return False

    def _load_configuration(self) -> bool:
        """Load configuration from STORAGE (no user input)"""
        try:
            # Load settings from STORAGE - uses saved or defaults
            settings = storage_layer.load_user_settings()
            
            # Configure MT5 connector with settings
            self.pyramid_structure, self.pyramid_style = mt5_connector.configure_from_settings(settings)
            self.symbol = mt5_connector.symbol
            self.fetch_interval = settings['fetch_interval']
            
            print(f"✅ Auto-configured: {self.symbol}, {self.pyramid_style}, {self.fetch_interval}s interval")
            return True
            
        except Exception as e:
            print(f"❌ Configuration failed: {e}")
            return False

    def _initialize_pyramid_engine(self):
        """Initialize pyramid engine with configuration"""
        pyramid_engine.configure_pyramid(
            symbol=self.symbol,
            pyramid_structure=self.pyramid_structure,
            pyramid_style=self.pyramid_style,
            utc_offset=mt5_connector.utc_offset
        )

    def _initialize_web_dashboard(self):
        """Initialize web dashboard and inject dependencies"""
        # FIXED: Inject main_launcher reference for symbol synchronization
        web_dashboard.inject_modules(mt5_connector, pyramid_engine, self)
        web_dashboard.setup_flask_app()
        web_dashboard.start_flask_server()

    def _load_initial_data(self) -> bool:
        """Load initial market data (ALL timeframes) - FIXED: Uses current symbol"""
        try:
            print(f"📥 Loading initial data for {self.symbol}...")
            
            # FIXED: Use self.symbol instead of hardcoded "EURUSD"
            raw_data = mt5_connector.fetch_all_timeframes(self.symbol)
            
            if not raw_data:
                print("❌ No data fetched")
                return False
            
            # Calculate momentum analysis for all timeframes
            pyramid_data = {}
            for tf in raw_data:
                if not raw_data[tf].empty:
                    pyramid_data[tf] = pyramid_engine.calculate_momentum_analysis(raw_data[tf])
                else:
                    print(f"⚠️  No data for {tf}")
                    pyramid_data[tf] = raw_data[tf]
            
            # Build pyramid JSON (uses only pyramid structure for display)
            pyramid_json = pyramid_engine.build_pyramid_json(pyramid_data)
            
            # Save pyramid data to storage
            storage_layer.save_pyramid_data(pyramid_json)
            
            # Update dashboard with ALL data
            web_dashboard.update_dashboard_data(raw_data, pyramid_json)
            
            print(f"✅ Initial data loaded: {len(pyramid_json.get('blocks', []))} blocks, {len(raw_data)} timeframes")
            return True
            
        except Exception as e:
            print(f"❌ Initial data loading failed: {e}")
            return False

    # ===========================================================
    # 🔄 MAIN COLLECTOR LOOP - FIXED VERSION
    # ===========================================================
    def collector_loop(self):
        """Main data collection and processing loop - FIXED: Dynamic symbol support"""
        print(f"\n🚀 Starting MEGA FLOWZ Data Collector...")
        print(f"   Symbol: {self.symbol}")
        print(f"   Pyramid: {self.pyramid_style} → {' → '.join(self.pyramid_structure)}")
        print(f"   All Timeframes: {', '.join(config.ALL_TIMEFRAMES)}")
        print(f"   Fetch interval: {self.fetch_interval}s")
        print(f"   Dashboard URL: http://127.0.0.1:{web_dashboard.dashboard_port}")
        print(f"   Press Ctrl+C to stop\n")
        
        # Open browser after a short delay
        threading.Timer(2, web_dashboard.open_browser).start()
        
        iteration = 1
        while not self.stop_event.is_set():
            # Wait for next cycle
            time.sleep(self.fetch_interval)
            if self.stop_event.is_set():
                break
                
            try:
                # FIXED: Use current symbol dynamically (supports symbol changes)
                current_symbol = self.symbol
                raw_data = mt5_connector.fetch_all_timeframes(current_symbol)
                
                if raw_data:
                    # Process data through pyramid engine
                    pyramid_data = {}
                    for tf in raw_data:
                        if not raw_data[tf].empty:
                            pyramid_data[tf] = pyramid_engine.calculate_momentum_analysis(raw_data[tf])
                    
                    # Build pyramid JSON (only shows pyramid structure)
                    pyramid_json = pyramid_engine.build_pyramid_json(pyramid_data)
                    
                    # Save to storage
                    storage_layer.save_pyramid_data(pyramid_json)
                    
                    # Update dashboard with ALL data
                    web_dashboard.update_dashboard_data(raw_data, pyramid_json)
                    
                    print(f"✅ Update #{iteration} @ {datetime.now().strftime('%H:%M:%S')} - {len(pyramid_json.get('blocks', []))} blocks, {len(raw_data)} TFs")
                    iteration += 1
                else:
                    print(f"❌ Update #{iteration} failed - no data")
                    
            except Exception as e:
                print(f"❌ Update error: {e}")
                time.sleep(60)  # Wait longer on error

    # ===========================================================
    # 🎮 SYSTEM CONTROL
    # ===========================================================
    def start(self):
        """Start the main system"""
        if self.running:
            print("⚠️  System already running")
            return
            
        if not self.initialize_system():
            print("❌ System failed to initialize")
            return
            
        self.running = True
        
        # Start collector thread
        self.collector_thread = threading.Thread(target=self.collector_loop, daemon=True)
        self.collector_thread.start()
        
        # Start health monitoring
        self._start_health_monitoring()
        
        print("\n🎯 System operational. Monitoring module health...")
        print("   Press Ctrl+C to shutdown gracefully\n")
        
        # Main thread just waits for shutdown
        try:
            while not self.stop_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop the system gracefully"""
        if not self.running:
            return
            
        print("\n⏹️  Shutdown signal received...")
        self.stop_event.set()
        self.running = False
        
        self._shutdown_system()

    def _start_health_monitoring(self):
        """Start background health monitoring"""
        def health_monitor():
            check_count = 0
            while not self.stop_event.is_set():
                time.sleep(30)  # Check every 30 seconds
                if self.stop_event.is_set():
                    break
                    
                mt5_health = "connected" if mt5_connector.connected else "disconnected"
                blocks_count = len(pyramid_engine.latest_pyramid.get('blocks', []))
                
                print(f"❤️  Health Check #{check_count}: MT5={mt5_health}, Blocks={blocks_count}, Uptime: {check_count * 30}s")
                check_count += 1
        
        health_thread = threading.Thread(target=health_monitor, daemon=True)
        health_thread.start()

    def _shutdown_system(self):
        """Perform complete system shutdown"""
        print("\n🔴 Initiating system shutdown...")
        
        # Stop collector thread
        if self.collector_thread and self.collector_thread.is_alive():
            self.collector_thread.join(timeout=5)
        
        # Shutdown MT5
        mt5_connector.safe_shutdown()
        
        # Cleanup dashboard
        web_dashboard.cleanup()
        
        print("✅ System shutdown complete")
        print("👋 MEGA FLOWZ terminated successfully")

    # ===========================================================
    # 📊 SYSTEM STATUS
    # ===========================================================
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            'running': self.running,
            'symbol': self.symbol,
            'pyramid_style': self.pyramid_style,
            'pyramid_structure': self.pyramid_structure,
            'fetch_interval': self.fetch_interval,
            'mt5_connected': mt5_connector.connected,
            'dashboard_running': web_dashboard.setup_done,
            'latest_blocks': len(pyramid_engine.latest_pyramid.get('blocks', [])),
            'last_update': datetime.now().isoformat()
        }

# ===============================================================
# 🧩 GLOBAL SHUTDOWN HANDLERS
# ===============================================================
def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print(f"\n🛑 Received shutdown signal {signum}")
    launcher.stop()
    sys.exit(0)

def safe_shutdown():
    """Safe shutdown procedure"""
    try:
        mt5_connector.safe_shutdown()
        print("🔌 Safe shutdown completed")
    except:
        pass

# Register shutdown handlers
atexit.register(safe_shutdown)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ===============================================================
# 🎬 APPLICATION ENTRY POINT
# ===============================================================
if __name__ == "__main__":
    launcher = MainLauncher()
    
    try:
        launcher.start()
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        launcher.stop()
    finally:
        safe_shutdown()