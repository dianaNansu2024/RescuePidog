from picamera2 import Picamera2
import cv2, time, numpy as np, os, datetime
from modules.detection import detect_humans

# Directory to save snapshots
SAVE_PATH = os.path.join(os.path.dirname(__file__), "../snapshots")
os.makedirs(SAVE_PATH, exist_ok=True)

# Globals
last_save_time = 0
SAVE_INTERVAL = 10  # seconds between saves
detected_human_count = 0

# Initialize PiCamera
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()
time.sleep(1)

def generate_video_stream():
    global last_save_time, detected_human_count

    while True:
        try:
            # Capture a frame
            frame = picam2.capture_array()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Detect humans
            humans = detect_humans(frame)
            detected_human_count = len(humans)

            # Draw boxes
            for (x1, y1, x2, y2) in humans:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

            # Save frame if human detected
            if humans and (time.time() - last_save_time > SAVE_INTERVAL):
                filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S.jpg")
                cv2.imwrite(os.path.join(SAVE_PATH, filename), frame)
                last_save_time = time.time()

            # Overlay count
            cv2.putText(frame, f"Humans: {detected_human_count}", (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # Encode to JPEG and yield
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(0.05)

        except Exception as e:
            print(f"❌ Camera stream error: {e}")
            continue

def get_human_status():
    return {"count": detected_human_count, "alert": detected_human_count > 0}
