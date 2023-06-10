from machine import Pin
import time



# GPIO configuration for KEY module
# KEY -> GPIO3
gpio_num_KEY = 3
key = Pin(gpio_num_KEY, Pin.IN, Pin.PULL_UP) # Set GPIO as Input, Pull-up mode

# GPIO configuration for LED module
# LED -> GPIO10
# LED is in "current sink" configuration, 
# Which means logic=1 -> turn off, logic=0 -> turn on
gpio_num_LED = 10
led = Pin(gpio_num_LED, Pin.OUT) # Set GPIO as Output

# GPIO configuration for Pico's onboard LED
led_pico = Pin('LED', Pin.OUT) # Set GPIO as Output



### Superloop
while True:
    # Task 1 : Polling button status
    button_status = key.value()

    # Task 2 : Blinking Pico's LED
    led_pico.toggle()
    time.sleep(1)

    # Task 3 : Toggle module's LED (GPIO10)
    if button_status == 0:
        while not key.value():
            time.sleep(0.01)
        led.toggle()

