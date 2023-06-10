from machine import Pin
from machine import ADC
from machine import Timer
from neopixel import NeoPixel
from oled import *
import time
import heapq



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

def task4_handler(tim):
    global fq
    heapq.heappush(fq, 4)



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

# RGB LED
rgb_led_num = 22
rgb_led_pin = Pin(rgb_led_num, Pin.OUT)
rgb_led     = NeoPixel(rgb_led_pin, 1)

# OLED Display
OLED = OLED_1inch5()
OLED.fill(0x0)
OLED.text("Start!", 1, 64, OLED.white)
OLED.show()



############## Interrupt Request Setup ################
# Timer for each tasks
tick_period_ms_task1 = 500  # Set time duration (ms) per tick
tick_period_ms_task3 = 50   # Set time duration (ms) per tick
tick_period_ms_task4 = 100 # Set time duration (ms) per tick
tim_task1 = Timer()
tim_task3 = Timer()
tim_task4 = Timer()
tim_task1.init(period=tick_period_ms_task1, mode=Timer.PERIODIC, callback=task1_handler)
tim_task3.init(period=tick_period_ms_task3, mode=Timer.PERIODIC, callback=task3_handler)
tim_task4.init(period=tick_period_ms_task4, mode=Timer.PERIODIC, callback=task4_handler)
# Set interrupt mode for task2
key.irq(trigger=Pin.IRQ_FALLING,handler=task2_handler)



######################### Tasks #########################
# Task1 : Blinking onboard LED (GREEN) every 1 second
def task1():
    global led_green
    led_green.toggle()

# Task2 : Glowing LED (Red) whenever the KEY is pressed
def task2():
    global key
    global led_red
    led_red.toggle()

# Task3 : Control the brighness of RGB_LED module (Set to Blue color) with VOL_ADJ module
def task3():
    global knob
    global brightness
    global rgb_led
    brightness = knob.read_u16()/65535*100
    red = 0
    green = 0
    blue = int(brightness)
    if blue > 100: blue = 100;
    rgb_led[0]=(red,green,blue)
    rgb_led.write()
   
# Task4 : Display brightness of RGB_LED on OLED display for every 3 second
def task4():
    global brightness
    global OLED
    OLED.fill(0x0)
    OLED.text("brightness=" + str(int(brightness)), 1, 64, OLED.white)
    OLED.show()



################### Main Program ###################
# Initialize global variable for tasks
brightness = 0
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
        elif fn == 4:
            task4()
    except IndexError:
        pass
    except:
        print("Something went wrong")

