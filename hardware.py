import uasyncio as asyncio
from asyn import Event
import sys
import pid
import math

setpoint = 0
timer_event = Event()
temperature = 10
RELAY_CICLE_SEC = 10

P = 0.2
I = 0.001
D= 0.0
mypid = pid.PID(P, I, D)


if sys.platform == 'esp8266':
	from machine import ADC, Pin
	adc = ADC(0)
	relay = Pin()

async def heater(timer_event, setpoint):
	while True:
		await timer_event	
		print('start heating')	
		print('setpoint={}'.format(setpoint))
		while timer_event.is_set():		
			if timer_event.value() > 0:
				timer_event.set(timer_event.value() - RELAY_CICLE_SEC)
				print(timer_event.value())
				mypid.setpoint = setpoint
				mypid.update(temperature)
				u = mypid.output
				if u > RELAY_CICLE_SEC:
					u = RELAY_CICLE_SEC
				# temp = temp - u
				print('u={}'.format(u))
				print('relay ON')
				await asyncio.sleep(u) 
				print('relay OFF')
				await asyncio.sleep(RELAY_CICLE_SEC - u)
			else:
				timer_event.clear()
				print('stop timer')

async def sensor():
	i=1
	while True:
		await asyncio.sleep(1)
		# volume = adc.read()
		# temperature = termistor(volume)
		# temperature = int(100 * math.sin(i/360))
		# i += 1
		print('temperature = {}'.format(temperature))
