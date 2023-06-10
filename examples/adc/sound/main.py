from machine import Pin
from machine import ADC
import time



# Global variable
task1_ready = False
task2_ready = False



def key_handler(pin):
    global task2_ready
    #print("button at KEY module is pressed!")
    # Set task ready flag
    if task2_ready == False:
        task2_ready = True

def start_record(record_buf, nsample, sample_rate):
    #print("recording in RAM...")
    for n in range(nsample):
        sound = sound_sensor.read_u16()
        record_buf.append(sound)
        time.sleep(1/sample_rate)
    #print("recording finished")

def display_record(record_buf):
    if (not record_buf is None) and len(record_buf) > 0:
        for n in range(len(record_buf)):
            # Send recorded sample to UART or just print it!
            # Send as CSV format, etc.
            #print("record:{}".format(record_buf[n]))
            print(record_buf[n])
        #print("record ends here")



# GPIO configuration for KEY module
# KEY -> GPIO3
# IO interrupt is used
gpio_num_KEY = 3
key = Pin(gpio_num_KEY, Pin.IN, Pin.PULL_UP) # Set GPIO as Input, Pull-up mode

# Set interrupt mode for GPIO
# Falling Edge type
key.irq(trigger=Pin.IRQ_FALLING,handler=key_handler)
# Initialize ADC for the analog output of sound sensor
# The Output is from LM386 amplifier
gpio_sound = 26
sound_sensor = ADC(Pin(gpio_sound))

# Initialize GPIO input for the digital sound sensor
# The Output is from LM393 comparator
gpio_sound_detect = 21
sound_detector = Pin(gpio_sound_detect, Pin.IN)



# Superloop
sample_rate=4000 # 4 kHz
nsample=1000
buf = []
while True:
    # Task 1 : Record sound by reading the analog voltage from sound sensor
    #print("Start task1 : record")
    buf = []
    start_record(buf, nsample, sample_rate)
    time.sleep(0.1)

    # Task 2 : Print the recorded sound
    if task2_ready:
        display_record(buf)
        task2_ready = False

