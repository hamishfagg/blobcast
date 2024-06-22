#!/usr/bin/python

# import alsaaudio, time, audioop
from rpi_hardware_pwm import HardwarePWM
import time

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


pwm = HardwarePWM(pwm_channel=0, hz=25_000, chip=0)
pwm.start(50) # full duty cycle

time.sleep(5)

pwm.stop()