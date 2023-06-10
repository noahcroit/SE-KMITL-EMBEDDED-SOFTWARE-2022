from machine import Pin
from machine import Timer
from machine import PWM
import time
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



############### Hardware Initialize ################
# GPIO configuration for LED module
# LED -> GPIO10
# LED is in "current sink" configuration, Which means logic=1 -> turn off, logic=0 -> turn on
gpio_num_LED = 10
led_red = Pin(gpio_num_LED, Pin.OUT) # Set GPIO as Output
led_red.value(1) # Turn off RED LED

# GPIO configuration for Pico's onboard LED
led_green = Pin('LED', Pin.OUT) # Set GPIO as Output
led_green.value(0) # Turn off Green LED

# PWM for Servo motor
pwm_servo = PWM(Pin(22))
pwm_servo.freq(50)

# WiFi Setup
wlan = network.WLAN(network.STA_IF)
wlan.active(True)



######### PWM for Servo Motor ##########
def angle_to_servo_pwm(angle_z):
    duty_16u_max = 65536
    w = 0.006*angle_z + 1.54
    return int(w*duty_16u_max/20.0)



################ MQTT ################
def sub_cb(topic, msg):
    global q_angle
    print("New message on topic {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(msg)
    q_angle.append(msg)

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
client.set_callback(sub_cb)
mqtt_connected = False



############## Interrupt Request Setup ################
# Timer for each tasks
tick_period_ms_task1 = 3000   # Set time duration (ms) per tick
tick_period_ms_task2 = 100    # Set time duration (ms) per tick
tick_period_ms_task3 = 5000   # Set time duration (ms) per tick
tim_task1 = Timer()
tim_task2 = Timer()
tim_task3 = Timer()
tim_task1.init(period=tick_period_ms_task1, mode=Timer.PERIODIC, callback=task1_handler)
tim_task2.init(period=tick_period_ms_task2, mode=Timer.PERIODIC, callback=task2_handler)
tim_task3.init(period=tick_period_ms_task3, mode=Timer.PERIODIC, callback=task3_handler)
#key.irq(trigger=Pin.IRQ_FALLING,handler=task4_handler)



######################### Tasks #########################
def task1():
    global mqtt_connected
    if mqtt_connected:
        topic_sub = b"node-gyro/angle-z"
        client.subscribe(topic_sub)

def task2(queue_angle):
    global pwm_servo
    val=None
    try:
        val = queue_angle.pop()
        val = float(val)
        d = angle_to_servo_pwm(val)
        if d > 65535:
            d = 65535
        pwm_servo.duty_u16(d)
        print("angle z={}, duty={}".format(val, d))

        
    except Exception as e:
        print("Angle Z's queue is empty")
        print(e)

def task3():
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
                mqtt_connect()
                mqtt_connected = True
                led_red.value(0)
                print("Connected to MQTT broker!")
                topic_sub = b"node-gyro/angle-z"
                client.subscribe(topic_sub)
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
            task3()
    except IndexError:
        pass
    except:
        print("Something went wrong")

