# Python script to turn on/off the onboard leds

#!/usr/bin/env python
from time import sleep
import os

# Disable current function of the led
os.system("echo gpio | sudo tee /sys/class/leds/led1/trigger")

# Turn on (1), wait 3 seconds, then off (0), wait 3 seconds, on the PWR LED.
os.system("echo 1 | sudo tee /sys/class/leds/led1/brightness")
sleep(3)
os.system("echo 0 | sudo tee /sys/class/leds/led1/brightness")
sleep(3)

# Revert the PWR LED back to 'under-voltage detect' mode.
os.system("echo input | sudo tee /sys/class/leds/led1/trigger")
