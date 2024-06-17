#!/usr/bin/python

import alsaaudio, time, audioop

print("pcms:")
print(alsaaudio.pcms())

# Open the device in blocking capture mode.
inp = alsaaudio.PCM(
  type=alsaaudio.PCM_CAPTURE,
  rate=8000,
  channels=1,
  device="hw:CARD=Loopback,DEV=1",
  periodsize=160)

while True:
  # Read data from device
  l,data = inp.read()
  if l:
    # Return the maximum of the absolute value of all samples in a fragment.
    print(audioop.max(data, 2))