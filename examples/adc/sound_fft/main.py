from machine import Pin
from machine import ADC
import time



# Initialize ADC for the analog output of sound sensor
# The Output is from LM386 amplifier
gpio_sound = 26
sound_sensor = ADC(Pin(gpio_sound))

# Initialize GPIO input for the digital sound sensor
# The Output is from LM393 comparator
gpio_sound_detect = 21
sound_detector = Pin(gpio_sound_detect, Pin.IN)



def start_record(record_buf, nsample, sample_rate):
    print("recording in RAM...")
    for i in range(nsample):
        voltage_sound = sound_sensor.read_u16()*3.3/65535
        record_buf.append(voltage_sound)
        time.sleep(1/sample_rate)
    print("recording finished")

# Superloop
task2_ready = False
print("sound demo")
while True:
    # Task 1 : Read the digital output from sound sensor
    if not sound_detector.value():
        print("sound is detected!")
        task2_ready = True
    else:
        print("no sound...")
        task2_ready = False
    
    # Task 2 : Read the analog voltage from sound sensor
    #          When sound is detected (from DO of sound sensor)
    if task2_ready:
        sample_rate=1000
        buf = []
        start_record(buf, 2000, sample_rate)
    #voltage_sound = ldr.read_u16()*3.3/65535

    # Task 3 : Display
    #print("LDR voltage = {0:.2f}V, VOL ADJ voltage = {1:.2f}V ".format(voltage_ldr, voltage_knob))

    # Sleep
    time.sleep(1)
