# 👻 Ghost Detector Project (Fake Sensor Simulation)

This is a fun AI-style ghost detector that simulates EMF, temperature, and motion to detect a “ghost”.

# 📁 Folder Structure
ghost-detector/
│
├── main.py
├── sensors.py
├── ghost_logic.py
├── sound.py
├── utils.py
├── index.html
└── README.md

 # 🐍 1) main.py
from sensors import read_emf, read_temp, read_motion
from ghost_logic import detect_ghost
from utils import print_status
from sound import play_sound

print("👻 Ghost Detector Started...\n")

while True:
    emf = read_emf()
    temp = read_temp()
    motion = read_motion()

    is_ghost = detect_ghost(emf, temp, motion)

    print_status(emf, temp, motion, is_ghost)

    if is_ghost:
        play_sound()

    input("\nPress Enter to scan again...\n")

# 🐍 2) sensors.py
import random

def read_emf():
    return random.randint(0, 100)

def read_temp():
    return random.uniform(15.0, 35.0)

def read_motion():
    return random.choice([True, False])

 # 🐍 3) ghost_logic.py
def detect_ghost(emf, temp, motion):
    if emf > 70 and temp < 20 and motion:
        return True
    return False

# 🐍 4) sound.py
def play_sound():
    print("🔊 BEEP! Ghost Presence Detected!")

# 🐍 5) utils.py
def print_status(emf, temp, motion, ghost):
    print("EMF Level:", emf)
    print("Temperature:", round(temp, 2), "°C")
    print("Motion Detected:", motion)

    if ghost:
        print("👻 GHOST FOUND!")
    else:
        print("✅ No Ghost Detected.")

# 🌐 index.html
<!DOCTYPE html>
<html>
<head>
<title>Ghost Detector</title>
<style>
body {
    font-family: Arial;
    background: black;
    color: lime;
    text-align: center;
    padding-top: 50px;
}
button {
    padding: 15px 30px;
    font-size: 18px;
    cursor: pointer;
}
</style>
</head>
<body>

<h1>👻 Ghost Detector</h1>
<p>Click to Scan for Ghost</p>
<button onclick="scan()">SCAN</button>

<h2 id="result"></h2>

<script>
function scan(){
    let chance = Math.random();
    if(chance > 0.7){
        document.getElementById("result").innerText = "👻 GHOST DETECTED!";
    } else {
        document.getElementById("result").innerText = "No Ghost Found.";
    }
}
</script>

</body>
</html>

# 📘 README.md
  👻 Ghost Detector Project

A fun fake ghost detector using Python and HTML.

## Features
- EMF Sensor Simulation
- Temperature Drop Detection
- Motion Detection
- Ghost Logic
- Web UI Scanner

## Run Python App
```bash
python main.py

# Run Web App

Just open index.html in browser.

# Made By

Rajdip Saha
Web Developer | Python Developer


---

 # If you want, I can:
- Add sound effects  
- Make real sensor version  
- Make Flask web version  
- Design GitHub banner for you 😎
