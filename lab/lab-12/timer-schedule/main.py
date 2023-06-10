from machine import Pin
from machine import ADC
from machine import Timer
from neopixel import NeoPixel
from oled import *
import time



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
SYSTICK_MAX = 1000000
systick = 0
def key_handler(pin):
    global toggle_ready
    toggle_ready = True

def timer_handler(tim):
    global SYSTICK_MAX
    global systick
    systick += 1
    if systick > SYSTICK_MAX:
        systick = 0

# Timer for scheduler
tick_period_ms = 1 # Set time duration (ms) per tick
tim = Timer()
tim.init(period=tick_period_ms, mode=Timer.PERIODIC, callback=timer_handler)

# Set interrupt mode for GPIO
# Falling Edge type
key.irq(trigger=Pin.IRQ_FALLING,handler=key_handler)



######################### Tasks #########################
class TaskSchedule:
    def __init__(self, period, systick_max, callback, priority=0):
        self.period = period
        self.tick_previous=0
        self.systick_max = systick_max
        self.callback = callback
        self.priority = priority

    def updateTick(self, systick):
        self.tick_previous = systick

    def isready(self, systick):
        tick_diff=0
        if systick >= self.tick_previous:
            tick_diff = systick - self.tick_previous
        else:
            tick_diff = systick + systick_max - self.tick_previous
        
        if tick_diff >= self.period:
            return True
        return False

    def run(self):
        self.callback()

# Task1 : Blinking onboard LED (GREEN) every 1 second
def task1():
    global led_green
    led_green.toggle()

# Task2 : Glowing LED (Red) whenever the KEY is pressed
def task2():
    global key
    global led_red
    global toggle_ready
    if toggle_ready:
        led_red.toggle()
        toggle_ready = False

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



############### Main Program #################
t1 = TaskSchedule(period=500, systick_max=SYSTICK_MAX, callback=task1)
t2 = TaskSchedule(period=10,  systick_max=SYSTICK_MAX, callback=task2)
t3 = TaskSchedule(period=10,  systick_max=SYSTICK_MAX, callback=task3)
t4 = TaskSchedule(period=100, systick_max=SYSTICK_MAX, callback=task4)

# Initialize global variable for tasks
brightness = 0
toggle_ready = False

while True:
    # Task Scheduling, Check if task has already reached to its period to run 
    # task 1
    if t1.isready(systick):
        t1.run()
        t1.updateTick(systick)
    # task 2
    if t2.isready(systick):
        t2.run()
        t2.updateTick(systick)
    # task 3
    if t3.isready(systick):
        t3.run()
        t3.updateTick(systick)
    # task 4
    if t4.isready(systick):
        t4.run()
        t4.updateTick(systick)

