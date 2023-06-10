from machine import Pin
import _thread
import time

# GPIO configuration for LED module
# LED -> GPIO10
# LED is in "current sink" configuration, Which means logic=1 -> turn off, logic=0 -> turn on
gpio_num_LED = 10
led_red = Pin(gpio_num_LED, Pin.OUT) # Set GPIO as Output

# GPIO configuration for Pico's onboard LED
led_green = Pin('LED', Pin.OUT) # Set GPIO as Output



def task(num, period, led):
    while True:
        led.toggle()   
        time.sleep(period)



# Thread #2 as new thread
_thread.start_new_thread(task, (1, 2, led_green))

# Thread #1 as main thread
task(2, 3, led_red)


