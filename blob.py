#!/usr/bin/python

import alsaaudio, time, audioop
from timeit import default_timer as timer

# Open the device in blocking capture mode.
inp = alsaaudio.PCM(
  type=alsaaudio.PCM_CAPTURE,
  rate=8000,
  channels=1,
  device="hw:CARD=Loopback,DEV=1",
  periodsize=160)
tick = 0
while True:
  print(f"Time: {timer() - tick}")
  tick = timer()
  # Read data from device
  l,data = inp.read()
  if l:
    # Return the maximum of the absolute value of all samples in a fragment.
    print(audioop.max(data, 2))