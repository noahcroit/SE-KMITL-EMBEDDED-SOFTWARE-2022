from machine import Pin
from machine import ADC
import time



# Initialize ADC for light sensor (LDR)
gpio_ldr = 26
ldr = ADC(Pin(gpio_ldr))

# Initialize ADC for Knob (VOL ADJ)
gpio_knob = 27
knob = ADC(Pin(gpio_knob))



# Superloop
print("vol adj demo")
while True:
    # Task 1 : Read the analog voltage from volume's ADC
    voltage_ldr = ldr.read_u16()*3.3/65535

    # Task 2 : Read the analog voltage from volume's ADC
    voltage_knob = knob.read_u16()*3.3/65535

    # Task 3 : Display
    print("LDR voltage = {0:.2f}V, VOL ADJ voltage = {1:.2f}V ".format(voltage_ldr, voltage_knob))

    # Sleep
    time.sleep(1)
    
    
