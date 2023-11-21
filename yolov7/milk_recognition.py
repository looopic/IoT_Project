import time
import cv2

#from picamera2 import Picamera2
import detect_copy as detect
from whatsapp_api_client_python import API

def setup():
    greenAPI = API.GreenAPI(
    "7103878622", "2779d547032343e58e2fc9324d3613d0d9246872a26849058a")
    return greenAPI

#def capture_image(file_path):
    with Picamera2 as camera:
        camera.capture(file_path)

def detect_milk_bottles(file_path):
    results = detect.detect_objects(weights="yolov7-tiny.pt",source=file_path)

    return results

def send_message(count, file_path, api):
    if(count<=1):
        api.sending.sendFileByUpload(
            "41788454345@c.us",
            file_path,
            f"Number of milk bottles: {count}"
        )

def main():
    api=setup()
    file_path="large_7610845188967.jpg"
    while True:
        #capture_image(file_path)
        milk_bottle_count = detect_milk_bottles(file_path)
        print(f"Number of milk bottles: {milk_bottle_count}")
        send_message(milk_bottle_count, file_path, api)
        time.sleep(60)

if __name__ == "__main__":
    main()