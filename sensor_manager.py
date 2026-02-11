"""
Ghost Detector - Sensor Manager
Handles all sensor readings and data collection
"""

import random
import time
import math
from threading import Thread, Lock
from datetime import datetime, timedelta

class SensorManager:
    def __init__(self):
        self.running = False
        self.thread = None
        self.lock = Lock()
        self.sensors = {
            'emf': {'value': 0.0, 'min': 0, 'max': 100, 'unit': 'mG'},
            'temperature': {'value': 72.0, 'min': 40, 'max': 90, 'unit': '°F'},
            'humidity': {'value': 45.0, 'min': 20, 'max': 80, 'unit': '%'},
            'pressure': {'value': 1013.0, 'min': 980, 'max': 1030, 'unit': 'hPa'},
            'spectral': {'value': 0.0, 'min': 0, 'max': 1000, 'unit': 'MHz'},
            'motion': {'value': 0.0, 'min': 0, 'max': 100, 'unit': ''}
        }
        
        self.start_time = None
        self.calibration_offset = {
            'emf': 0,
            'temperature': 0,
            'humidity': 0,
            'pressure': 0,
            'spectral': 0,
            'motion': 0
        }
        
        self.ghost_activity = 0
        self.activity_patterns = []
        
    def start(self):
        """Start the sensor reading thread"""
        if not self.running:
            self.running = True
            self.start_time = datetime.now()
            self.thread = Thread(target=self._read_sensors_loop)
            self.thread.daemon = True
            self.thread.start()
            print("✅ Sensor manager started")
    
    def stop(self):
        """Stop the sensor reading thread"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
            print("✅ Sensor manager stopped")
    
    def _read_sensors_loop(self):
        """Main sensor reading loop"""
        while self.running:
            self._update_sensor_readings()
            time.sleep(0.5)  # Update every 500ms
    
    def _update_sensor_readings(self):
        """Update all sensor readings with simulated data"""
        with self.lock:
            # Simulate ghost activity patterns
            self.ghost_activity = self._calculate_ghost_activity()
            
            # EMF Reader - sensitive to ghost activity
            self.sensors['emf']['value'] = self._simulate_emf()
            
            # Temperature - drops near ghosts
            self.sensors['temperature']['value'] = self._simulate_temperature()
            
            # Humidity - changes with paranormal activity
            self.sensors['humidity']['value'] = self._simulate_humidity()
            
            # Barometric pressure - fluctuates
            self.sensors['pressure']['value'] = self._simulate_pressure()
            
            # Spectral analyzer - detects ghost frequencies
            self.sensors['spectral']['value'] = self._simulate_spectral()
            
            # Motion detector - EMF motion correlation
            self.sensors['motion']['value'] = self._simulate_motion()
    
    def _simulate_emf(self):
        """Simulate EMF readings"""
        base = 25 + random.uniform(-5, 5)
        if self.ghost_activity > 50:
            base += self.ghost_activity * 0.7
        if random.random() < 0.1:  # 10% chance of EMF spike
            base += random.uniform(30, 50)
        return max(0, min(100, base + self.calibration_offset['emf']))
    
    def _simulate_temperature(self):
        """Simulate temperature readings"""
        base = 72 + random.uniform(-1, 1)
        if self.ghost_activity > 60:
            base -= self.ghost_activity * 0.3  # Cold spots
        if self.sensors['emf']['value'] > 70:
            base -= 10  # EMF correlates with cold
        return max(40, min(90, base + self.calibration_offset['temperature']))
    
    def _simulate_humidity(self):
        """Simulate humidity readings"""
        base = 45 + random.uniform(-3, 3)
        if self.ghost_activity > 40:
            base += random.uniform(5, 15)  # Humidity often rises
        return max(20, min(80, base + self.calibration_offset['humidity']))
    
    def _simulate_pressure(self):
        """Simulate barometric pressure"""
        base = 1013 + random.uniform(-2, 2)
        if self.ghost_activity > 70:
            base += random.uniform(-10, -5)  # Pressure drops
        return max(980, min(1030, base + self.calibration_offset['pressure']))
    
    def _simulate_spectral(self):
        """Simulate spectral analyzer readings"""
        base = random.uniform(100, 300)
        if self.ghost_activity > 30:
            # Ghost frequencies in specific ranges
            base += math.sin(time.time()) * 50 + self.ghost_activity * 5
        if random.random() < 0.15:  # 15% chance of EVP/spike
            base += random.uniform(200, 400)
        return max(0, min(1000, base + self.calibration_offset['spectral']))
    
    def _simulate_motion(self):
        """Simulate motion detection"""
        base = random.uniform(0, 20)
        if self.ghost_activity > 50:
            base += self.ghost_activity * 0.4
        if self.sensors['emf']['value'] > 60:
            base += 30  # Motion follows EMF
        return max(0, min(100, base + self.calibration_offset['motion']))
    
    def _calculate_ghost_activity(self):
        """Calculate ghost activity level"""
        # Time-based pattern (ghosts more active at night)
        current_hour = datetime.now().hour
        time_factor = 0
        if current_hour < 6 or current_hour > 20:  # Night time
            time_factor = 30
        
        # Random events
        random_activity = random.uniform(0, 40)
        
        # Cycle pattern
        cycle = (math.sin(time.time() * 0.1) + 1) * 15
        
        activity = time_factor + random_activity + cycle
        
        # Store pattern for analysis
        self.activity_patterns.append({
            'timestamp': datetime.now(),
            'level': activity
        })
        
        # Keep only last 100 patterns
        if len(self.activity_patterns) > 100:
            self.activity_patterns.pop(0)
        
        return min(100, activity)
    
    def get_all_readings(self):
        """Get current readings from all sensors"""
        with self.lock:
            readings = {}
            for sensor_name, sensor_data in self.sensors.items():
                readings[sensor_name] = round(sensor_data['value'], 1)
            return readings
    
    def get_sensor(self, sensor_name):
        """Get reading from specific sensor"""
        with self.lock:
            if sensor_name in self.sensors:
                return self.sensors[sensor_name]
            return None
    
    def calibrate(self):
        """Calibrate all sensors"""
        with self.lock:
            for sensor in self.calibration_offset:
                # Reset to baseline
                self.calibration_offset[sensor] = random.uniform(-2, 2)
            
            # Reset ghost activity
            self.ghost_activity = 0
            self.activity_patterns.clear()
            
            return "Calibration successful"
    
    def get_status(self):
        """Get sensor status"""
        return {name: "online" for name in self.sensors.keys()}
    
    def get_uptime(self):
        """Get system uptime"""
        if self.start_time:
            uptime = datetime.now() - self.start_time
            return str(uptime).split('.')[0]
        return "0:00:00"