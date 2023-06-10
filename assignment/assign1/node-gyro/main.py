from machine import Pin
from machine import Timer
import time
from dof import *
import network
from umqtt.simple import MQTTClient
import ubinascii



############### Task handler for Function-Queue ##############
# Setup Function-Queue
fq = []

def task1_handler(tim):
    global fq
    fq.append(1)
def task2_handler(pin):
    global fq
    fq.append(2)

def task3_handler(tim):
    global fq
    fq.append(3)

def task4_handler(tim):
    global fq
    fq.append(4)



############### Hardware Initialize ################
# GPIO configuration for KEY module
# KEY -> GPIO3
# IO interrupt is used
gpio_num_KEY = 3
key = Pin(gpio_num_KEY, Pin.IN, Pin.PULL_UP) # Set GPIO as Input, Pull-up mode

# GPIO configuration for LED module
# LED -> GPIO10
# LED is in "current sink" configuration, Which means logic=1 -> turn off, logic=0 -> turn on
gpio_num_LED = 10
led_red = Pin(gpio_num_LED, Pin.OUT) # Set GPIO as Output
led_red.value(1) # Turn off Red LED

# GPIO configuration for Pico's onboard LED
led_green = Pin('LED', Pin.OUT) # Set GPIO as Output
led_green.value(0) # Turn off Green LED

# DOF sensor (gyro & accel)
angle_z = 0
gyro_sample_time = 0.1
qmi8658=QMI8658()

# WiFi Setup
wlan = network.WLAN(network.STA_IF)
wlan.active(True)


################ MQTT ################
def mqtt_connect():
    global client
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))

def mqtt_publish(topic, msg):
    global client
    client.publish(topic, msg, retain=False, qos=0)

mqtt_server = 'broker.hivemq.com'
#mqtt_server = '192.168.82.82'
client_id = ubinascii.hexlify(machine.unique_id())
client = MQTTClient(client_id, mqtt_server, port=1883, keepalive=3600)
mqtt_connected = False



############## Interrupt Request Setup ################
# GPIO Interrupt for task1
key.irq(trigger=Pin.IRQ_FALLING,handler=task1_handler)

# Timer for each tasks
tick_period_ms_task2 = 100     # Set time duration (ms) per tick
tick_period_ms_task3 = 100     # Set time duration (ms) per tick
tick_period_ms_task4 = 5000   # Set time duration (ms) per tick
tim_task2 = Timer()
tim_task3 = Timer()
tim_task4 = Timer()
tim_task2.init(period=tick_period_ms_task2, mode=Timer.PERIODIC, callback=task2_handler)
tim_task3.init(period=tick_period_ms_task3, mode=Timer.PERIODIC, callback=task3_handler)
tim_task4.init(period=tick_period_ms_task4, mode=Timer.PERIODIC, callback=task4_handler)



######################### Tasks #########################
def task1():
    global angle_z
    angle_z = 0 # Reset the Angle value

def task2(queue_angle):
    global qmi8658
    global gyro_sample_time
    global angle_z
    xyz=qmi8658.Read_XYZ()
    velocity_z = xyz[5]
    angle_z = angle_z + velocity_z*gyro_sample_time
    queue_angle.append(angle_z)

def task3(queue_angle):
    val=None
    try:
        val = queue_angle.pop()
        print("angle z={}".format(val))
        if mqtt_connected:
            topic = b"node-gyro/angle-z"
            msg = str(val).encode()
            mqtt_publish(topic, msg)

    except Exception as e:
        print("Angle Z's queue is empty")
        print(e)

def task4():
    global wlan
    global mqtt_connected
    global led_green
    global led_red
    SSID = "moto-noah"
    PWD  = "1029384756"
    #SSID = "ASUS_for_ICT"
    #PWD  = "ictadmin"
    if not wlan.isconnected():
        led_green.value(0)
        print("Disconnected, connecting...")
        wlan.connect(SSID, PWD)
    
    if wlan.isconnected():
        led_green.value(1)
        print("WIFI connected")
        if not mqtt_connected:
            try:
                client = mqtt_connect()
                mqtt_connected = True
                led_red.value(0)
                print("Connected to MQTT broker!")
            except OSError as e:
                print(e)
                mqtt_connected = False
                led_red.value(1)


    


################### Main Program ###################
# Superloop
q_angle = []
while True:
    # Checking if there is a task in the Q, ready to be run
    try:
        fn = fq.pop()
        if fn == 1:
            task1()
        elif fn == 2:
            task2(q_angle)
        elif fn == 3:
            task3(q_angle)
        elif fn == 4:
            task4()
    except IndexError:
        pass
    except:
        print("Something went wrong")

