"""
Ghost Detector - Data Logger
Logs and manages historical detection data
"""

import json
import os
from datetime import datetime, timedelta
from collections import deque
import threading

class DataLogger:
    def __init__(self, log_file="ghost_detector_logs.json"):
        self.log_file = log_file
        self.logs = deque(maxlen=1000)
        self.events = deque(maxlen=500)
        self.lock = threading.Lock()
        self._load_logs()
        
    def _load_logs(self):
        """Load existing logs from file"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    data = json.load(f)
                    for log in data.get('logs', []):
                        self.logs.append(log)
                    for event in data.get('events', []):
                        self.events.append(event)
                print(f"📂 Loaded {len(self.logs)} logs from file")
        except Exception as e:
            print(f"⚠️ Could not load logs: {e}")
    
    def save_logs(self):
        """Save logs to file"""
        try:
            with open(self.log_file, 'w') as f:
                json.dump({
                    'logs': list(self.logs),
                    'events': list(self.events),
                    'last_save': datetime.now().isoformat()
                }, f, indent=2)
            print(f"💾 Saved {len(self.logs)} logs to file")
        except Exception as e:
            print(f"⚠️ Could not save logs: {e}")
    
    def log_reading(self, sensor_data, analysis):
        """Log a sensor reading and analysis"""
        with self.lock:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'sensors': sensor_data,
                'analysis': analysis
            }
            self.logs.append(log_entry)
            
            # Log significant events
            if analysis['probability'] > 60:
                self.log_event({
                    'type': 'significant_detection',
                    'timestamp': log_entry['timestamp'],
                    'probability': analysis['probability'],
                    'ghost_type': analysis.get('ghost_type'),
                    'evidence': analysis.get('evidence', [])
                })
    
    def log_event(self, event_data):
        """Log a specific event"""
        with self.lock:
            event_entry = {
                'timestamp': event_data.get('timestamp', datetime.now().isoformat()),
                'type': event_data.get('type', 'info'),
                'data': event_data
            }
            self.events.append(event_entry)
    
    def get_recent_logs(self, count=50):
        """Get most recent logs"""
        with self.lock:
            return list(self.logs)[-count:]
    
    def get_logs_by_date(self, date):
        """Get logs for a specific date"""
        with self.lock:
            result = []
            for log in self.logs:
                log_date = log['timestamp'][:10]  # YYYY-MM-DD
                if log_date == date:
                    result.append(log)
            return result
    
    def get_events(self, event_type=None, limit=100):
        """Get logged events"""
        with self.lock:
            if event_type:
                return [e for e in list(self.events)[-limit:] 
                       if e['data'].get('type') == event_type]
            return list(self.events)[-limit:]
    
    def generate_report(self, hours=24):
        """Generate a report for the last X hours"""
        with self.lock:
            cutoff = datetime.now() - timedelta(hours=hours)
            recent_logs = [
                log for log in self.logs 
                if datetime.fromisoformat(log['timestamp']) > cutoff
            ]
            
            if not recent_logs:
                return {"error": "No data available for this period"}
            
            # Calculate statistics
            probabilities = [log['analysis']['probability'] for log in recent_logs]
            avg_probability = sum(probabilities) / len(probabilities) if probabilities else 0
            
            detections = [log for log in recent_logs 
                         if log['analysis']['probability'] > 50]
            
            ghost_types = {}
            for log in detections:
                ghost_type = log['analysis'].get('ghost_type')
                if ghost_type:
                    ghost_types[ghost_type] = ghost_types.get(ghost_type, 0) + 1
            
            report = {
                'period': f"Last {hours} hours",
                'total_readings': len(recent_logs),
                'avg_activity': round(avg_probability, 1),
                'total_detections': len(detections),
                'max_probability': max(probabilities) if probabilities else 0,
                'min_probability': min(probabilities) if probabilities else 0,
                'ghost_type_breakdown': ghost_types,
                'most_active_hour': self._get_most_active_hour(recent_logs),
                'generated': datetime.now().isoformat()
            }
            
            return report
    
    def _get_most_active_hour(self, logs):
        """Find the hour with most activity"""
        hour_count = {}
        for log in logs:
            hour = datetime.fromisoformat(log['timestamp']).hour
            hour_count[hour] = hour_count.get(hour, 0) + 1
        
        if hour_count:
            max_hour = max(hour_count.items(), key=lambda x: x[1])
            return f"{max_hour[0]:02d}:00 - {max_hour[0]:02d}:59 ({max_hour[1]} readings)"
        return "Unknown"
    
    def export_to_csv(self, filename="ghost_data_export.csv"):
        """Export data to CSV format"""
        import csv
        
        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['timestamp', 'emf', 'temperature', 'humidity', 
                            'pressure', 'spectral', 'motion', 'probability', 
                            'ghost_type', 'activity_level']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for log in list(self.logs)[-500:]:  # Last 500 entries
                    row = {
                        'timestamp': log['timestamp'],
                        'emf': log['sensors'].get('emf', ''),
                        'temperature': log['sensors'].get('temperature', ''),
                        'humidity': log['sensors'].get('humidity', ''),
                        'pressure': log['sensors'].get('pressure', ''),
                        'spectral': log['sensors'].get('spectral', ''),
                        'motion': log['sensors'].get('motion', ''),
                        'probability': log['analysis'].get('probability', ''),
                        'ghost_type': log['analysis'].get('ghost_type', ''),
                        'activity_level': log['analysis'].get('activity_level', '')
                    }
                    writer.writerow(row)
            
            return f"✅ Data exported to {filename}"
        except Exception as e:
            return f"❌ Export failed: {e}"
    
    def clear_old_logs(self, days=7):
        """Clear logs older than specified days"""
        with self.lock:
            cutoff = datetime.now() - timedelta(days=days)
            original_count = len(self.logs)
            
            self.logs = deque(
                [log for log in self.logs 
                 if datetime.fromisoformat(log['timestamp']) > cutoff],
                maxlen=1000
            )
            
            removed = original_count - len(self.logs)
            return f"🗑️ Removed {removed} old logs"
        

        