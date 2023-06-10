from machine import Pin
from machine import ADC
from neopixel import NeoPixel
from oled import *
import time



def key_handler(pin):
    global toggle_ready
    toggle_ready = True



# GPIO configuration for KEY module
# KEY -> GPIO3
# IO interrupt is used
gpio_num_KEY = 3
key = Pin(gpio_num_KEY, Pin.IN, Pin.PULL_UP) # Set GPIO as Input, Pull-up mode

# Set interrupt mode for GPIO
# Falling Edge type
key.irq(trigger=Pin.IRQ_FALLING,handler=key_handler)

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



# Task1 : Blinking onboard LED (GREEN) in every 1 second
def task1():
    global led_green
    led_green.toggle()
    time.sleep(0.5)

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
    time.sleep(3)



# Initialize global variable for tasks
brightness = 0
toggle_ready = False
while True:
    task1()
    task2()
    task3()
    task4()

