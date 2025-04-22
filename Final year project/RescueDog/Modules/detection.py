import cv2
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models")
PROTOTXT = os.path.join(MODEL_DIR, "MobileNetSSD_deploy.prototxt")
CAFFEMODEL = os.path.join(MODEL_DIR, "MobileNetSSD_deploy.caffemodel")

if not os.path.exists(PROTOTXT) or not os.path.exists(CAFFEMODEL):
    raise FileNotFoundError("MobileNetSSD model files missing!")

net = cv2.dnn.readNetFromCaffe(PROTOTXT, CAFFEMODEL)
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

def detect_humans(frame):
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    h, w = frame.shape[:2]
    results = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        idx = int(detections[0, 0, i, 1])
        if confidence > 0.5 and CLASSES[idx] == "person":
            box = detections[0, 0, i, 3:7] * [w, h, w, h]
            results.append(tuple(map(int, box)))
    return results
