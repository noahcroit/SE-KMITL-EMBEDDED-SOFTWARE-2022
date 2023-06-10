import network
import time
import machine
from machine import Pin
from umqtt.simple import MQTTClient
import ubinascii


# GPIO configuration for Pico's onboard LED
led_green = Pin('LED', Pin.OUT) # Set GPIO as Output

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("moto-noah","1029384756")

while not wlan.isconnected():
    time.sleep(5)
    print("connecting...")
print("WIFI connect success")


topic_sub = b'pico-noah-led'
def sub_cb(topic, msg):
    global led_green

    print("New message on topic {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(msg)
    if msg == "on":
        led_green.value(1)
    elif msg == "off":
        led_green.value(0)

def mqtt_connect():
    #mqtt_server = 'broker.hivemq.com'
    mqtt_server = '192.168.82.82'
    client_id = ubinascii.hexlify(machine.unique_id())
    #client = MQTTClient(client_id, mqtt_server, port=1880, user='mqtt', password='mqtt1234', keepalive=60)
    client = MQTTClient(client_id, mqtt_server, port=1883, keepalive=3600)
    client.set_callback(sub_cb)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to MQTT Broker. Reconnecting...')
    time.sleep(5)
    return mqtt_connect()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

while True:
    client.subscribe(topic_sub)
    time.sleep(1)
