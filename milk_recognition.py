import time
#from picamera2 import Picamera2
from whatsapp_api_client_python import API
from detect_copy import detect_milk_bottles_yolo

def setup():
    greenAPI = API.GreenAPI(
        "7103878622", "2779d547032343e58e2fc9324d3613d0d9246872a26849058a")
    return greenAPI

""" def capture_image(file_path):
    with Picamera2() as camera:
        camera.capture(file_path) """

def detect_milk_bottles(file_path):
    return detect_milk_bottles_yolo(file_path)

def send_message(count, file_path, api):
    if count <= 1:
        api.sending.sendFileByUpload(
            "41788454345@c.us",
            file_path,
            f"Number of milk bottles: {count}"
        )

def main():
    api = setup()
    file_path = "large_7610845188967.jpg"
    
    while True:
        try:
            #capture_image(file_path)
            milk_bottle_count = detect_milk_bottles(file_path)
            print(f"Number of milk bottles: {milk_bottle_count}")
            send_message(milk_bottle_count, file_path, api)
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred: {e}")
            # Add more specific exception handling as needed

if __name__ == "__main__":
    main()