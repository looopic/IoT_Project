import paho.mqtt.client as mqtt

MQTT_SERVER = "127.0.0.1"

MQTT_TEMP = "sensor/temp"
MQTT_HUMI = "sensor/humid"
MQTT_PRES = "sensor/press"

def on_connect(client,userdata,flags,rc):
	print("Connected with result code "+str(rc))
	client.subscribe(MQTT_TEMP)
	client.subscribe(MQTT_HUMI)
	client.subscribe(MQTT_PRES)

def on_message(client,userdata,msg):
	print(msg.topic+ " "+str(msg.payload))

client=mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()
