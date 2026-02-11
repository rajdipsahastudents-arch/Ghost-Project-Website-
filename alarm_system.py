"""
Ghost Detector - Alarm System
Handles alerts and notifications for ghost detection
"""

import time
import threading
import winsound  # Windows only, replace for other OS
from datetime import datetime
from enum import Enum

class AlarmLevel(Enum):
    NONE = 0
    WARNING = 1
    CRITICAL = 2
    EMERGENCY = 3

class AlarmSystem:
    def __init__(self):
        self.alarm_state = AlarmLevel.NONE
        self.alarm_history = []
        self.active_alerts = []
        self.lock = threading.Lock()
        self.alert_thread = None
        self.running = True
        
    def trigger_alarm(self, analysis):
        """Trigger alarm based on ghost analysis"""
        probability = analysis.get('probability', 0)
        
        with self.lock:
            previous_state = self.alarm_state
            
            if probability > 90:
                self.alarm_state = AlarmLevel.EMERGENCY
                self._add_alert("🚨 EMERGENCY: Extreme paranormal activity detected!", "emergency")
            elif probability > 80:
                self.alarm_state = AlarmLevel.CRITICAL
                self._add_alert("⚠️ CRITICAL: Ghost confirmed - immediate attention required", "critical")
            elif probability > 60:
                self.alarm_state = AlarmLevel.WARNING
                self._add_alert("📢 WARNING: Significant paranormal activity detected", "warning")
            else:
                self.alarm_state = AlarmLevel.NONE
            
            # Log state change
            if previous_state != self.alarm_state:
                self._log_state_change(previous_state, self.alarm_state, analysis)
                
            # Trigger sound alert if state increased
            if self.alarm_state.value > previous_state.value:
                self._play_alert_sound(self.alarm_state)
    
    def _add_alert(self, message, alert_type):
        """Add an alert to the active list"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'type': alert_type,
            'acknowledged': False
        }
        self.active_alerts.append(alert)
        
        # Keep only last 20 active alerts
        if len(self.active_alerts) > 20:
            self.active_alerts = self.active_alerts[-20:]
    
    def _log_state_change(self, previous, current, analysis):
        """Log alarm state changes"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'previous_state': previous.name,
            'current_state': current.name,
            'probability': analysis.get('probability'),
            'ghost_type': analysis.get('ghost_type')
        }
        self.alarm_history.append(log_entry)
        
        # Keep history manageable
        if len(self.alarm_history) > 100:
            self.alarm_history = self.alarm_history[-100:]
    
    def _play_alert_sound(self, level):
        """Play audible alert based on alarm level"""
        def play_sound():
            if level == AlarmLevel.WARNING:
                for _ in range(3):
                    winsound.Beep(800, 200)
                    time.sleep(0.1)
            elif level == AlarmLevel.CRITICAL:
                for _ in range(5):
                    winsound.Beep(1000, 300)
                    time.sleep(0.1)
            elif level == AlarmLevel.EMERGENCY:
                for _ in range(8):
                    winsound.Beep(1200, 200)
                    winsound.Beep(800, 200)
                    time.sleep(0.1)
        
        # Play sound in separate thread
        sound_thread = threading.Thread(target=play_sound)
        sound_thread.daemon = True
        sound_thread.start()
    
    def acknowledge_alert(self, alert_index):
        """Mark an alert as acknowledged"""
        with self.lock:
            if 0 <= alert_index < len(self.active_alerts):
                self.active_alerts[alert_index]['acknowledged'] = True
                return True
        return False
    
    def clear_alarms(self):
        """Clear all active alarms"""
        with self.lock:
            self.alarm_state = AlarmLevel.NONE
            self.active_alerts = []
            self._add_alert("✅ All alarms cleared", "info")
            return "Alarms cleared"
    
    def get_status(self):
        """Get current alarm system status"""
        with self.lock:
            unacknowledged = sum(1 for alert in self.active_alerts 
                               if not alert['acknowledged'])
            
            return {
                'current_level': self.alarm_state.name,
                'active_alerts': len(self.active_alerts),
                'unacknowledged': unacknowledged,
                'recent_history': self.alarm_history[-5:] if self.alarm_history else []
            }
    
    def get_alerts(self, include_acknowledged=False):
        """Get list of active alerts"""
        with self.lock:
            if include_acknowledged:
                return self.active_alerts
            return [a for a in self.active_alerts if not a['acknowledged']]
    
    def simulate_emergency(self):
        """Simulate emergency for testing"""
        analysis = {
            'probability': 95,
            'ghost_type': 'Poltergeist',
            'evidence': ['EMF Spike: 85 mG', 'Cold Spot: 45°F', 'Spectral Anomaly: 750 MHz']
        }
        self.trigger_alarm(analysis)
        return "🚨 Emergency simulation activated"
    
    def shutdown(self):
        """Shutdown alarm system"""
        self.running = False
        self.clear_alarms()
        print("🔕 Alarm system shutdown")