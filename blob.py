#!/usr/bin/python

# import alsaaudio, time, audioop
from rpi_hardware_pwm import HardwarePWM
import time
import sys

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

if len(sys.argv) == 1:
    print("blob.py <freq> <duty> <time>")
    sys.exit(0)

pwm = HardwarePWM(pwm_channel=0, chip=0, hz=float(sys.argv[1]))
pwm.start(float(sys.argv[2]))

time.sleep(float(sys.argv[3]))

pwm.stop()