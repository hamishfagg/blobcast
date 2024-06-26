#!/usr/bin/python

# import alsaaudio, time, audioop
from rpi_hardware_pwm import HardwarePWM
import time
import sys
from itertools import cycle
from easing_functions import QuadEaseInOut

# Open the device in blocking capture mode.
# This setup means we get a bunch of data from alsa every 0.02s or every 50th of a second.
# inp = alsaaudio.PCM(
#   type=alsaaudio.PCM_CAPTURE,
#   rate=8000,
#   channels=1,
#   device="hw:CARD=Loopback,DEV=1",
#   periodsize=160)
# tick = 0
# while True:
#   # Read data from device
#   l,data = inp.read()
#   if l:
#     # Return the maximum of the absolute value of all samples in a fragment.
#     print(audioop.max(data, 2))

def idle(pwm):
    IDLE_CYCLE_TIME = 3.0  # Seconds
    IDLE_CYCLE_STEPS = 10  # Steps in each direction. So total steps is 2* this number
    IDLE_MAX_DUTY = 60
    IDLE_MIN_DUTY = 50

    easing = QuadEaseInOut(start=IDLE_MIN_DUTY, end=IDLE_MAX_DUTY)

    pwm.change_frequency(65)
    pwm.start(IDLE_MAX_DUTY)
    desc_range = range(IDLE_MAX_DUTY, IDLE_MIN_DUTY, -int((IDLE_MAX_DUTY-IDLE_MIN_DUTY)/IDLE_CYCLE_STEPS))
    asc_range = range(IDLE_MIN_DUTY, IDLE_MAX_DUTY, int((IDLE_MAX_DUTY-IDLE_MIN_DUTY)/IDLE_CYCLE_STEPS))
    
    steps = [*desc_range, *asc_range]
    print(steps)
    steps = [(s-IDLE_MIN_DUTY)/(IDLE_MAX_DUTY-IDLE_MIN_DUTY) for s in steps]
    eased_steps = list(map(easing, steps))
    print(eased_steps)

    for duty in cycle(eased_steps):
        time.sleep(IDLE_CYCLE_TIME/(IDLE_CYCLE_STEPS*2))
        pwm.change_duty_cycle(duty)

# if len(sys.argv) == 1:
#   print("blob.py <freq> <duty> <time>")
#   sys.exit(0)


pwm = HardwarePWM(pwm_channel=0, chip=0, hz=60.0)
try:
    idle(pwm)
except:
    pwm.stop()
    raise
# pwm.start(float(sys.argv[2]))

# time.sleep(float(sys.argv[3]))