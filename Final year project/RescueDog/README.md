🐶 RescueDog — Autonomous Search & SLAM Robot
RescueDog is a Raspberry Pi-powered quadruped robot that combines real-time video streaming, human detection, autonomous movement, and SLAM mapping. It’s designed to assist in search and rescue environments by detecting humans and mapping unknown terrain using ultrasonic sensors.

🚀 Features
📸 Live Camera Feed via web interface

👤 Human Detection with MobileNetSSD (OpenCV DNN)

🗺️ SLAM Mapping using head-mounted ultrasonic sweeps

🐾 Autonomous Patrol Mode with real-time obstacle detection

🎮 Manual Control via web interface

💾 Snapshot Saving on human detection

🔴 Flashing Alert Dot in UI when human is detected

⚙️ Expandable with Google Drive or return-home mode

📦 Folder Structure
bash
Copy code
RescueDog/
├── app.py                   # Flask app
├── modules/                # All functional logic
│   ├── camera.py           # Camera stream + human detection
│   ├── detection.py        # MobileNetSSD detection logic
│   ├── pidog_control.py    # Manual controls for PiDog
│   ├── autonomous.py       # Patrol and obstacle avoidance logic
│   └── slam.py             # SLAM grid mapping
├── snapshots/              # Saved image captures
├── templates/
│   └── index.html          # Web frontend
├── models/                 # MobileNetSSD .prototxt and .caffemodel
└── README.md
🛠️ Installation
Prerequisites:
Raspberry Pi OS (Bookworm recommended)

PiDog robot installed and tested

Python 3.9+

OpenCV (with DNN support)

Flask

PyCamera2

Setup:
bash
Copy code
sudo apt update
sudo apt install python3-opencv libatlas-base-dev
pip install flask picamera2
Also ensure your MobileNetSSD files are inside models/:

MobileNetSSD_deploy.prototxt

MobileNetSSD_deploy.caffemodel

▶️ Running the App
From your project directory:

bash
Copy code
python3 app.py
Open the web UI in your browser:

cpp
Copy code
http://<your-pi-ip>:5000
Example: http://192.168.137.213:5000

🧠 Web Interface
🔴 Red alert = human detected

👀 Live video from PiCamera2

🗺️ SLAM map updates in real time

🎮 Controls: Forward, Left, Right, Backward, Autonomous (Trot)

📸 Snapshots are saved when a person is detected

📸 Snapshot Access
Browse saved images from:

arduino
Copy code
http://<your-pi-ip>:5000/snapshots
🧪 Future Ideas
🔋 Live battery and CPU monitoring

☁️ Cloud uploads (Google Drive, S3)

🔁 Return to base functionality

🎙️ Voice or gesture-based commands

🤝 Credits
Built with 💡 by Nansubuga Diana
Based on the Sunfounder PiDog SDK