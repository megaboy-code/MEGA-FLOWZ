# ===============================================================
# 💾 STORAGE LAYER - SIMPLIFIED DATA PERSISTENCE
# ===============================================================

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
import config

class StorageLayer:
    def __init__(self):
        self.data_dir = "data"
        self.settings_file = os.path.join(self.data_dir, "user_settings.json")
        self._ensure_directories()
        print("💾 Storage Layer initialized")

    def _ensure_directories(self):
        """Create necessary directories"""
        os.makedirs(self.data_dir, exist_ok=True)

    # ===========================================================
    # 🎛️ USER SETTINGS MANAGEMENT
    # ===========================================================
    def load_user_settings(self) -> Dict[str, Any]:
        """Load user settings from file or return defaults"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    settings = config.DEFAULT_SETTINGS.copy()
                    settings.update(saved_settings)
                    return settings
        except Exception as e:
            print(f"⚠️ Error loading settings: {e}")
        
        return config.DEFAULT_SETTINGS.copy()

    def save_user_settings(self, settings: Dict[str, Any]) -> bool:
        """Save user settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            print("💾 User settings saved")
            return True
        except Exception as e:
            print(f"❌ Error saving settings: {e}")
            return False

    # ===========================================================
    # 🏗️ PYRAMID DATA STORAGE - SIMPLIFIED
    # ===========================================================
    def save_pyramid_data(self, pyramid_data: Dict[str, Any]):
        """Save pyramid data to JSON file - Simple overwrite"""
        try:
            symbol = pyramid_data.get('symbol', 'unknown')
            filename = f"pyramid_{symbol}.json"
            filepath = os.path.join(self.data_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(pyramid_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Pyramid data saved: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving pyramid data: {e}")
            return False

    def load_pyramid_for_symbol(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Load pyramid data for specific symbol"""
        try:
            filename = f"pyramid_{symbol}.json"
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading pyramid for {symbol}: {e}")
        
        return None

    # ===========================================================
    # 🔔 ALERTS STORAGE
    # ===========================================================
    def save_alert(self, alert_data: Dict[str, Any]):
        """Save trading alert"""
        try:
            alerts_file = os.path.join(self.data_dir, "alerts.json")
            alerts = self.load_alerts()
            
            alert_data['id'] = datetime.now().strftime("%Y%m%d%H%M%S")
            alert_data['created'] = datetime.now().isoformat()
            alerts.append(alert_data)
            
            with open(alerts_file, 'w', encoding='utf-8') as f:
                json.dump(alerts, f, indent=2, ensure_ascii=False)
                
            print(f"🔔 Alert saved: {alert_data.get('message', 'Unknown')}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving alert: {e}")
            return False

    def load_alerts(self) -> list:
        """Load all alerts"""
        try:
            alerts_file = os.path.join(self.data_dir, "alerts.json")
            if os.path.exists(alerts_file):
                with open(alerts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        
        return []

# Singleton instance
storage_layer = StorageLayer()