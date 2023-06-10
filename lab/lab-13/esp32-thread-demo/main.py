from machine import Pin
import _thread
import time




def task(num, period):
    while True:
        #print("hello task {}".format(task_num))
        print("hello task {}".format(num))
        time.sleep(period)



_thread.start_new_thread(task, (1, 1))
_thread.start_new_thread(task, (2, 0.5))
_thread.start_new_thread(task, (3, 2))
while True:
    # Need to check the status of all threads in here
    print("hello main")
    time.sleep(3)


