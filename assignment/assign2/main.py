from machine import Pin
from machine import ADC
from machine import Timer
from neopixel import NeoPixel
import time
import heapq
from motor import *


############### Task handler for Function-Queue ##############
# Setup Function-Queue using heapq
fq = []
heapq.heapify(fq)

def task1_handler(tim):
    global fq
    heapq.heappush(fq, 1)

def task2_handler(pin):
    global fq
    heapq.heappush(fq, 2)

def task3_handler(tim):
    global fq
    heapq.heappush(fq, 3)



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

# GPIO configuration for Pico's onboard LED
led_green = Pin('LED', Pin.OUT) # Set GPIO as Output

# ADC for VOL_ADJ module
gpio_knob = 27
knob = ADC(Pin(gpio_knob)) 

# Motor Driver
m = MotorDriver()
speed = 0


############## Interrupt Request Setup ################
# Timer for each tasks
tick_period_ms_task1 = 500   # Set time duration (ms) per tick
tick_period_ms_task2 = 1000   # Set time duration (ms) per tick
tim_task1 = Timer()
tim_task2 = Timer()
tim_task1.init(period=tick_period_ms_task1, mode=Timer.PERIODIC, callback=task1_handler)
tim_task2.init(period=tick_period_ms_task2, mode=Timer.PERIODIC, callback=task2_handler)
key.irq(trigger=Pin.IRQ_FALLING,handler=task3_handler)



######################### Tasks #########################
def task1():
    global speed
    # read knob for motor speed
    speed = knob.read_u16()/65535*100

def task2():
    global m
    print("run motor, speed={}".format(speed))
    m.MotorRun('MA', 'forward', speed, 1)

def task3():
    pass


################### Main Program ###################
# Superloop
while True:
    # Checking if there is a task in the Q, ready to be run
    try:
        fn = heapq.heappop(fq)
        if fn == 1:
            task1()
        elif fn == 2:
            task2()
        elif fn == 3:
            task3()
    except IndexError:
        pass
    except:
        print("Something went wrong")

