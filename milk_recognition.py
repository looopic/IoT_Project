import time
#from picamera2 import Picamera2
from whatsapp_api_client_python import API
from detect_picamera import main as detect
from inky.auto import auto
from PIL import Image, ImageDraw
from update_image import draw_image
import paho.mqtt.client as mqtt


MQTT_SERVER = "127.0.0.1"

MQTT_TEMP = "sensor/temp"
MQTT_HUMI = "sensor/humid"
MQTT_PRES = "sensor/press"
pre,hum,tem=0,0,0

def on_connect(client,userdata,flags,rc):
	print("Connected with result code "+str(rc))
	client.subscribe(MQTT_TEMP)
	client.subscribe(MQTT_HUMI)
	client.subscribe(MQTT_PRES)
def on_message(client,userdata,msg):
    if(msg.topic==MQTT_TEMP):
        tem=str(msg.payload)
    elif(msg.topic==MQTT_PRES):
        pre=str(msg.payload)
    elif(msg.topic==MQTT_HUMI):
        hum=str(msg.payload)

	
client=mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)


def setup():
    display = auto()
    resolution=display.resolution
    greenAPI = API.GreenAPI(
        "7103878622", "2779d547032343e58e2fc9324d3613d0d9246872a26849058a")
    return greenAPI, display, resolution

""" def capture_image(file_path):
    with Picamera2() as camera:
        camera.capture(file_path) """

def send_message(count, file_path, api):
    if count <= 1:
        api.sending.sendFileByUpload(
            "41788454345@c.us",
            file_path,
            f"Number of milk bottles: {count}"
        )


def main():
    api, display, resolution = setup()
    file_path = "large_7610845188967.jpg"
    labels="coco_labels.txt"
    model="detect.tflite"
    
    while True:
        try:
            #capture_image(file_path)
            milk_bottle_count = detect(labels, model, file_path)
            print(f"Number of milk bottles: {milk_bottle_count}")
            client.loop()
            send_message(milk_bottle_count, file_path, api)
            display.set_image(draw_image(resolution,hum,pre,tem,milk_bottle_count))
            display.show()
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred: {e}")
            # Add more specific exception handling as needed

if __name__ == "__main__":
    main()