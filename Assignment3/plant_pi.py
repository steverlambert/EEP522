#!/usr/bin/env python

import time
from gpiozero import MCP3008
import smbus
import wiringpi



#### Setup Servo ####

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

#### Pump Pin ####
wiringpi.pinMode(17, 1)

#### Setup ADC pins #####
ai0 = MCP3008(0) # moisture sensor

#### Setup I2C #####
bus = smbus.SMBus(1)
addr = 0x48

#write registers
als_conf_0 = 0x00
pow_sav = 0x03

#Read registers
als = 0x04

# These settings will provide the range for the sensor: (0 - 15099 lx)
confValues = [0x00, 0x18] # 1/4 gain, 100ms IT (Integration Time)

power_save_mode = [0x00, 0x00] # Clear values

bus.write_i2c_block_data(addr, als_conf_0, confValues)
bus.write_i2c_block_data(addr, pow_sav, power_save_mode)


max = 0

def read_lux():
	time.sleep(.04) # 40ms
	word = bus.read_word_data(addr,als)
	gain = 0.2304 # gain=1/4 and int time=100ms, max lux=15099 lux
	val = word * gain
	valcorr = (6.0135E-13*val**4)-(9.392E-9*val**3)+(8.1488E-5*val**2)+(1.0023E0*val)
	valcorr = round(valcorr,1) #Round corrected value for presentation
	#val = round(val,1) #Round value for presentation
	return valcorr

def read_moisture(sec):
	total = 0
	print("Finding ave. moisture over %i secs" %sec)
	for i in range(sec):
		time.sleep(1)
		total += ai0.value
	return total / sec
	
def run_servo_scan():
	delay = .2
	
	
	# reset to starting position
	wiringpi.pwmWrite(18, 50)
	time.sleep(delay)
	wiringpi.pwmWrite(18,0)
	time.sleep(delay)
	
	max_lux = 0
	max_pulse = 0
	l = 0
	
	for pulse in range(50, 250, 15):
		print("pulse: ", pulse)
		wiringpi.pwmWrite(18, pulse)
		time.sleep(delay)
		#print("stopping")
		wiringpi.pwmWrite(18,0)
		l = read_lux()
		if l > max_lux:
			max_lux = l
			max_pulse = pulse
		print("lux: ", l)
		time.sleep(delay)
	
	# set servo to max lighting location	
	wiringpi.pwmWrite(18, max_pulse)
	time.sleep(delay)
	wiringpi.pwmWrite(18,0)
	time.sleep(delay)
	
def run_pump(secs):
	wiringpi.digitalWrite(17, 0) # sets port 24 to 0 (0V, off)  
	time.sleep(1)                    # wait 10s  
	wiringpi.digitalWrite(17, 1) # sets port 24 to 1 (3V3, on)  
	time.sleep(secs)                    # wait 10s  
	wiringpi.digitalWrite(17, 0) # sets port 24 to 0 (0V, off)  

moisture = read_moisture(1)
print("Moisture: %f" %moisture)

#if moisture > 0.55:
#	run_pump(5)

lux = read_lux()
print("Light level: %f" %lux)

run_servo_scan()
	
