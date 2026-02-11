"""
Ghost Detector - Ghost Analyzer
Analyzes sensor data to detect paranormal activity
"""

import numpy as np
import random
import math
from datetime import datetime, timedelta
from collections import deque

class GhostAnalyzer:
    def __init__(self):
        self.detection_threshold = 60
        self.history = deque(maxlen=50)
        self.ghost_types = [
            "Poltergeist", "Wraith", "Phantom", "Specter", 
            "Banshee", "Apparition", "Shadow Person", "Orb",
            "Mist Entity", "Ectoplasm"
        ]
        
        self.evidence_weights = {
            'emf': 0.30,
            'temperature': 0.25,
            'spectral': 0.25,
            'motion': 0.15,
            'humidity': 0.03,
            'pressure': 0.02
        }
        
    def analyze(self, sensor_data):
        """
        Analyze sensor data for ghost activity
        Returns a comprehensive analysis of paranormal activity
        """
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'probability': 0,
            'ghost_type': None,
            'evidence': [],
            'confidence': 0,
            'activity_level': 'None',
            'recommendations': []
        }
        
        # Calculate probability based on multiple factors
        probability = self._calculate_probability(sensor_data)
        analysis['probability'] = round(probability, 1)
        
        # Determine activity level
        if probability < 30:
            analysis['activity_level'] = 'Low'
        elif probability < 60:
            analysis['activity_level'] = 'Moderate'
        elif probability < 80:
            analysis['activity_level'] = 'High'
        else:
            analysis['activity_level'] = 'Critical'
        
        # Identify ghost type if probability is high enough
        if probability > 40:
            analysis['ghost_type'] = self._identify_ghost_type(sensor_data)
            analysis['evidence'] = self._gather_evidence(sensor_data)
            analysis['confidence'] = round(self._calculate_confidence(sensor_data), 1)
            analysis['recommendations'] = self._generate_recommendations(analysis)
        
        # Store in history
        self.history.append(analysis)
        
        return analysis
    
    def _calculate_probability(self, data):
        """Calculate ghost probability from sensor data"""
        score = 0
        total_weight = 0
        
        # Weighted scoring system
        for sensor, weight in self.evidence_weights.items():
            if sensor in data:
                normalized_value = self._normalize_sensor(sensor, data[sensor])
                score += normalized_value * weight
                total_weight += weight
        
        if total_weight > 0:
            base_probability = (score / total_weight) * 100
        else:
            base_probability = 0
        
        # Add time-based modifier (ghosts more active at night)
        current_hour = datetime.now().hour
        time_modifier = 0
        if current_hour < 6 or current_hour > 20:
            time_modifier = 15
        elif current_hour < 8 or current_hour > 18:
            time_modifier = 5
        
        # Add pattern recognition
        pattern_modifier = self._analyze_patterns()
        
        probability = base_probability + time_modifier + pattern_modifier
        
        return max(0, min(100, probability))
    
    def _normalize_sensor(self, sensor, value):
        """Normalize sensor value to 0-1 range"""
        ranges = {
            'emf': (0, 100),
            'temperature': (40, 90),
            'humidity': (20, 80),
            'pressure': (980, 1030),
            'spectral': (0, 1000),
            'motion': (0, 100)
        }
        
        if sensor in ranges:
            min_val, max_val = ranges[sensor]
            # Invert temperature (colder = more paranormal)
            if sensor == 'temperature':
                normalized = 1 - ((value - min_val) / (max_val - min_val))
            else:
                normalized = (value - min_val) / (max_val - min_val)
            return max(0, min(1, normalized))
        
        return 0
    
    def _analyze_patterns(self):
        """Analyze historical patterns for ghost activity"""
        if len(self.history) < 10:
            return 0
        
        recent = list(self.history)[-10:]
        probabilities = [h['probability'] for h in recent]
        
        # Check for increasing trend
        if len(probabilities) > 1:
            trend = probabilities[-1] - probabilities[0]
            if trend > 20:
                return 15
            elif trend > 10:
                return 8
        
        return 0
    
    def _identify_ghost_type(self, data):
        """Identify the type of ghost based on evidence"""
        evidence_profile = {}
        
        # Build evidence profile
        if data.get('emf', 0) > 70:
            evidence_profile['emf'] = 'high'
        elif data.get('emf', 0) > 50:
            evidence_profile['emf'] = 'medium'
        
        if data.get('temperature', 72) < 50:
            evidence_profile['temperature'] = 'cold'
        
        if data.get('spectral', 0) > 600:
            evidence_profile['spectral'] = 'high_frequency'
        
        if data.get('motion', 0) > 60:
            evidence_profile['motion'] = 'active'
        
        # Match evidence to ghost types
        if 'cold' in evidence_profile.values() and 'high_frequency' in evidence_profile.values():
            return "Wraith"
        elif 'high' in evidence_profile.get('emf', '') and 'active' in evidence_profile.get('motion', ''):
            return "Poltergeist"
        elif 'high_frequency' in evidence_profile.get('spectral', ''):
            return "Specter"
        elif 'cold' in evidence_profile.get('temperature', ''):
            return "Phantom"
        elif 'active' in evidence_profile.get('motion', ''):
            return "Apparition"
        else:
            return random.choice(self.ghost_types)
    
    def _gather_evidence(self, data):
        """Gather evidence of paranormal activity"""
        evidence = []
        
        if data.get('emf', 0) > 50:
            evidence.append(f"EMF Spike: {data['emf']} mG")
        if data.get('temperature', 72) < 55:
            evidence.append(f"Cold Spot: {data['temperature']}°F")
        if data.get('spectral', 0) > 500:
            evidence.append(f"Spectral Anomaly: {data['spectral']} MHz")
        if data.get('motion', 0) > 50:
            evidence.append(f"Motion Detected: {data['motion']}%")
        if data.get('humidity', 45) > 65:
            evidence.append(f"Humidity Surge: {data['humidity']}%")
        if data.get('pressure', 1013) < 995:
            evidence.append(f"Pressure Drop: {data['pressure']} hPa")
        
        return evidence[:5]  # Return top 5 evidence
    
    def _calculate_confidence(self, data):
        """Calculate confidence level in detection"""
        confidence_factors = []
        
        # Multiple sensor correlation
        sensors_triggered = 0
        for sensor, threshold in [('emf', 60), ('temperature', 55), 
                                 ('spectral', 500), ('motion', 60)]:
            if data.get(sensor, 0) > threshold:
                sensors_triggered += 1
        
        confidence_factors.append(sensors_triggered * 15)
        
        # History consistency
        if len(self.history) > 5:
            recent_detections = sum(1 for h in list(self.history)[-5:] 
                                  if h['probability'] > 50)
            confidence_factors.append(recent_detections * 8)
        
        # Random factor for realism
        confidence_factors.append(random.uniform(5, 15))
        
        return min(100, sum(confidence_factors))
    
    def _generate_recommendations(self, analysis):
        """Generate investigation recommendations"""
        recommendations = []
        
        prob = analysis['probability']
        
        if prob > 80:
            recommendations.append("⚠️ IMMEDIATE EVACUATION RECOMMENDED")
            recommendations.append("Contact paranormal investigation team")
            recommendations.append("Set up additional recording equipment")
        elif prob > 60:
            recommendations.append("Maintain observation - activity increasing")
            recommendations.append("Deploy backup sensors")
            recommendations.append("Document all readings")
        elif prob > 40:
            recommendations.append("Continue monitoring")
            recommendations.append("Check sensor calibration")
            recommendations.append("Note environmental conditions")
        else:
            recommendations.append("Normal conditions")
            recommendations.append("Perform routine sensor check")
        
        return recommendations
    
    def generate_spectral_bands(self):
        """Generate spectral frequency bands for visualization"""
        bands = []
        base_frequency = random.uniform(20, 80)
        
        for i in range(20):
            if random.random() < 0.3:  # 30% chance of activity
                band = base_frequency + random.uniform(-10, 50)
            else:
                band = random.uniform(10, 40)
            
            bands.append(max(5, min(100, band)))
        
        return bands