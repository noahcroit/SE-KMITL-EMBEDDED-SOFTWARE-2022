from machine import Pin
import uasyncio
import time

# GPIO configuration for LED module
# LED -> GPIO10
# LED is in "current sink" configuration, Which means logic=1 -> turn off, logic=0 -> turn on
gpio_num_LED = 10
led_red = Pin(gpio_num_LED, Pin.OUT) # Set GPIO as Output

# GPIO configuration for Pico's onboard LED
led_green = Pin('LED', Pin.OUT) # Set GPIO as Output


# Coroutine: blink
async def blink(period, led):
    while True:
        led.toggle()   
        await uasyncio.sleep(period)


async def main():
    global led_red
    global led_green
    uasyncio.create_task(blink(1, led_red))
    uasyncio.create_task(blink(0.25, led_green))
    await uasyncio.sleep(10)

uasyncio.run(main())
