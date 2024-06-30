#!/usr/bin/python

import alsaaudio, time, audioop
from rpi_hardware_pwm import HardwarePWM
import time
import sys
from itertools import cycle
from easing_functions import QuadEaseInOut


# lows = 0-150
# mids = 150-4k
# highs = 4k-20k

LOOP_HZ = 50
SAMPLE_RATE = 48_000
AUDIO_SILENCE_THRESHOLD = 50
AUDIO_SILENCE_TIMEOUT = 5  # In loops. See LOOP_HZ above

# Idle setup:
IDLE_CYCLE_TIME = 3.0  # Seconds
IDLE_CYCLE_STEPS = 10  # Steps in each direction. So total steps is 2* this number
IDLE_MAX_DUTY = 60
IDLE_MIN_DUTY = 50

easing = QuadEaseInOut(start=IDLE_MIN_DUTY, end=IDLE_MAX_DUTY)

pwm = HardwarePWM(pwm_channel=0, chip=0, hz=60.0)
pwm.change_frequency(65)
pwm.start(IDLE_MAX_DUTY)

desc_range = range(IDLE_MAX_DUTY, IDLE_MIN_DUTY, -int((IDLE_MAX_DUTY-IDLE_MIN_DUTY)/IDLE_CYCLE_STEPS))
asc_range = range(IDLE_MIN_DUTY, IDLE_MAX_DUTY, int((IDLE_MAX_DUTY-IDLE_MIN_DUTY)/IDLE_CYCLE_STEPS))

steps = [*desc_range, *asc_range]
steps = [(s-IDLE_MIN_DUTY)/(IDLE_MAX_DUTY-IDLE_MIN_DUTY) for s in steps]
eased_steps = list(map(easing, steps))

idle_index = 0

def idle(pwm):
    global idle_index
    idle_index = (idle_index + 1) % len(eased_steps)
    pwm.change_duty_cycle(eased_steps[idle_index])


# Open the device in blocking capture mode.
# This setup means we get a bunch of data from alsa every 0.02s or every 50th of a second.
inp = alsaaudio.PCM(
    type=alsaaudio.PCM_CAPTURE,
    rate=SAMPLE_RATE,
    channels=1,
    device="hw:CARD=Loopback,DEV=1",
    periodsize=int(SAMPLE_RATE/LOOP_HZ))


silence_time = 0
try:
    while True:
        # Read data from device
        l, data = inp.read()
        if l:
            # Return the maximum of the absolute value of all samples in a fragment.
            max = audioop.max(data, 4)
            if max > AUDIO_SILENCE_THRESHOLD:
                silence_time = 0
                print("leaving idle")
            else:
                silence_time += 1

            if silence_time >= AUDIO_SILENCE_TIMEOUT:
                idle(pwm)

except:
    pwm.stop()
    raise
