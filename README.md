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
Copy
Edit
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
Copy
Edit
sudo apt update
sudo apt install python3-opencv libatlas-base-dev
pip install flask picamera2
Also ensure your MobileNetSSD files are inside models/:

MobileNetSSD_deploy.prototxt

MobileNetSSD_deploy.caffemodel

▶️ Running the App
From your project directory:

bash
Copy
Edit
python3 app.py
Open the web UI in your browser:

cpp
Copy
Edit
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
Copy
Edit
http://<your-pi-ip>:5000/snapshots
🧪 Future Ideas
🔋 Live battery and CPU monitoring

☁️ Cloud uploads (Google Drive, S3)

🔁 Return to base functionality

🎙️ Voice or gesture-based commands

🤝 Credits
Built with 💡 by [Your Name or Team]
Based on the Sunfounder PiDog SDK

Let me know if you'd like to include screenshots, a logo, or make this ready for GitHub publishing!






You said:
make this ready for github publishing


ChatGPT said:
Here's your polished, GitHub-ready README.md tailored for your RescueDog project — with proper markdown styling, badges, and GitHub best practices included.

🐶 RescueDog
A Raspberry Pi-powered quadruped robot for autonomous navigation, SLAM, and human detection. Built using the SunFounder PiDog and OpenCV.


✨ Features
🎥 Live camera streaming (PiCamera2)

👤 Real-time human detection (MobileNetSSD via OpenCV DNN)

🗺️ SLAM mapping with ultrasonic sensor

🤖 Autonomous patrol mode with obstacle avoidance

🎮 Manual directional control via web interface

🔴 Flashing red alert when humans are detected

📸 Automatic snapshots saved locally

🧠 Modular architecture (easy to expand)

📸 Demo

Replace the above link with your actual screenshot once uploaded!

🗂️ Project Structure
bash
Copy
Edit
RescueDog/
├── app.py                 # Flask web server
├── models/                # DNN models (MobileNetSSD)
├── modules/               # Core logic for each function
│   ├── camera.py          # Video + human detection
│   ├── detection.py       # OpenCV DNN detection
│   ├── autonomous.py      # Patrol + SLAM
│   ├── pidog_control.py   # Manual control interface
│   └── slam.py            # Grid-based SLAM logic
├── snapshots/             # Saved images when people are detected
├── templates/
│   └── index.html         # Web UI
└── README.md
🚀 Getting Started
🧰 Requirements
Raspberry Pi 4 / 5 with Raspberry Pi OS

PiDog robot (SunFounder)

Python 3.9+

PiCamera2

Flask

OpenCV (cv2) with DNN module

🛠️ Installation
bash
Copy
Edit
# Clone the repository
git clone https://github.com/yourusername/RescueDog.git
cd RescueDog

# Install dependencies
sudo apt update
sudo apt install python3-opencv libatlas-base-dev
pip install flask picamera2
Download MobileNetSSD:

bash
Copy
Edit
mkdir -p models/
wget -O models/MobileNetSSD_deploy.prototxt https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/MobileNetSSD_deploy.prototxt
wget -O models/MobileNetSSD_deploy.caffemodel https://github.com/chuanqi305/MobileNet-SSD/releases/download/v1.0/MobileNetSSD_deploy.caffemodel
▶️ Usage
Start the web server:

bash
Copy
Edit
python3 app.py
Then open in your browser:

cpp
Copy
Edit
http://<raspberry-pi-ip>:5000
You’ll see the live camera feed, SLAM map, movement controls, and status indicators.

🧪 Features Overview

Feature	Description
Camera Feed	Live PiCamera2 stream
Human Detection	OpenCV DNN with MobileNetSSD
SLAM	Grid map using ultrasonic readings
Patrol Mode	Detects and avoids obstacles
Manual Controls	Forward, Back, Left, Right, Trot
Snapshots	Saves image if human detected
Web Interface	Full control from browser
📁 Snapshots
To view stored images from detections:

arduino
Copy
Edit
http://<your-pi-ip>:5000/snapshots
🤖 Future Enhancements
🔋 Battery & CPU live stats

☁️ Cloud snapshot storage (Google Drive, S3, etc.)

🧭 Return-to-home logic with path tracing

📱 Mobile UI or voice control

📜 License
This project is licensed under the MIT License.

🙌 Acknowledgements
SunFounder PiDog

OpenCV DNN

Flask

You! 🧠✨

📬 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change or enhance.
