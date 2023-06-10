from machine import Pin
import uasyncio
import time



# Coroutine: Button
async def button(btn):
    print("wait for press")
    while btn.value() == 1:
        #await uasyncio.sleep(0.1)
        time.sleep(0.1)
    print("pressed!")

# Coroutine: blink
async def blink(led, period):
    while True:
        led.toggle()
        await uasyncio.sleep(period)


async def main():
    # GPIO configuration for LED module
    # LED -> GPIO10
    # LED is in "current sink" configuration, Which means logic=1 -> turn off, logic=0 -> turn on
    gpio_num_LED = 10
    led_red = Pin(gpio_num_LED, Pin.OUT) # Set GPIO as Output

    # GPIO configuration for Pico's onboard LED
    led_green = Pin('LED', Pin.OUT) # Set GPIO as Output

    # GPIO configuration for KEY module
    # KEY -> GPIO3
    # IO interrupt is used
    gpio_num_KEY = 3
    btn = Pin(gpio_num_KEY, Pin.IN, Pin.PULL_UP) # Set GPIO as Input, Pull-up mode

    uasyncio.create_task(blink(led_green, 1))
    uasyncio.create_task(blink(led_red, 4))
    uasyncio.create_task(button(btn))
    await uasyncio.sleep(20)

uasyncio.run(main())



