import time
import cv2

from picamera2 import Picamera2
from yolov7.detector import Detector
from whatsapp_api_client_python import API

def setup():
    detector = Detector('yolov7-tiny')
    greenAPI = API.GreenAPI(
    "7103878622", "2779d547032343e58e2fc9324d3613d0d9246872a26849058a")
    return detector, greenAPI

def capture_image(file_path):
    with Picamera2 as camera:
        camera.capture(file_path)

def detect_milk_bottles(detector,file_path):
    img=cv2.imread(file_path)
    results = detector.detect(img)
    milk_bottle_count=0

    for result in results:
        class_name = result['class_name']
        confidence = result['confidence']

        if class_name.lower() == 'bottle' and confidence > 0.2:  # You can adjust this threshold
            milk_bottle_count += 1

    return milk_bottle_count

def send_message(count, file_path, api):
    if(count<=1):
        api.sending.sendFileByUpload(
            "41788454345@c.us",
            file_path,
            f"Number of milk bottles: {count}"
        )

def main():
    detector, api=setup()
    file_path="capture.png"
    while True:
        capture_image(file_path)
        milk_bottle_count = detect_milk_bottles(detector, file_path)
        print(f"Number of milk bottles: {milk_bottle_count}")
        send_message(milk_bottle_count, file_path, api)
        time.sleep(60)

if __name__ == "__main__":
    main()