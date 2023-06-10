from machine import Pin
import time



# global variable
task2_ready = False



def key_handler(pin):
    global task2_ready
    print("button at KEY module is pressed!")
    if task2_ready == False:
        task2_ready = True



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
led = Pin(gpio_num_LED, Pin.OUT) # Set GPIO as Output

# GPIO configuration for Pico's onboard LED
led_pico = Pin('LED', Pin.OUT) # Set GPIO as Output



# Superloop
print("Wait for the key to be pressed")
while True:
    # Task 1 : Blinking Pico's LED
    led_pico.toggle()
    time.sleep(1)

    # Task 2 : Toggle module's LED (GPIO10)
    if task2_ready:
        print("task 2 running...")
        led.toggle()
        task2_ready = False
