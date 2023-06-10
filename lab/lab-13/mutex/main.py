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


lock = _thread.allocate_lock()

def task(num, period):
    while True:
        lock.acquire()
        print("This is thread {}".format(num))
        print(", Thread {} is running with period {}".format(num, period))
        lock.release()
        time.sleep(period)



# Thread #2 as new thread
_thread.start_new_thread(task, (2, 0.01, ))

# Thread #1 as main thread
task(1, 0.01)


