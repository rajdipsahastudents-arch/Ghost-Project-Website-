"""
Ghost Detector - Main Application
Entry point for the paranormal detection system
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import threading
import time

from sensor_manager import SensorManager
from ghost_analyzer import GhostAnalyzer
from data_logger import DataLogger
from alarm_system import AlarmSystem

app = FastAPI(title="Ghost Detector", description="Paranormal Activity Detection System")

# Initialize components
sensor_manager = SensorManager()
ghost_analyzer = GhostAnalyzer()
data_logger = DataLogger()
alarm_system = AlarmSystem()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize the detection system"""
    sensor_manager.start()
    print("👻 Ghost Detector System Started")
    print("📡 All sensors initialized")
    print("⚡ Ready to detect paranormal activity")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown the detection system"""
    sensor_manager.stop()
    data_logger.save_logs()
    print("👻 Ghost Detector System Shutdown")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML interface"""
    with open("index.html", "r") as f:
        return f.read()

@app.get("/api/sensors")
async def get_sensor_data():
    """Get current sensor readings"""
    try:
        sensor_data = sensor_manager.get_all_readings()
        
        # Analyze for ghost activity
        ghost_analysis = ghost_analyzer.analyze(sensor_data)
        
        # Log the data
        data_logger.log_reading(sensor_data, ghost_analysis)
        
        # Check if we need to trigger alarm
        if ghost_analysis['probability'] > 70:
            alarm_system.trigger_alarm(ghost_analysis)
        
        # Add spectral bands for visualization
        sensor_data['spectralBands'] = ghost_analyzer.generate_spectral_bands()
        
        return sensor_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/calibrate")
async def calibrate_sensors():
    """Calibrate all sensors"""
    try:
        result = sensor_manager.calibrate()
        return {"message": f"Sensors calibrated: {result}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
async def get_history():
    """Get historical detection data"""
    return data_logger.get_recent_logs(100)

@app.get("/api/status")
async def get_system_status():
    """Get system status"""
    return {
        "status": "operational",
        "sensors": sensor_manager.get_status(),
        "alarm": alarm_system.get_status(),
        "uptime": sensor_manager.get_uptime()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)