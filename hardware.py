import uasyncio as asyncio
from asyn import Event
import sys
import pid
import math


setpoint_event = Event()
timer_event = Event()
temp_event = Event()
temp_event.set(10)
temperature = 10
RELAY_CICLE_SEC = 5

P = 0.2
I = 0.01
D= 0.0
mypid = pid.PID(P, I, D)


if sys.platform == 'esp8266':
	from machine import ADC, Pin, PWM
	adc = ADC(0)
	led = Pin(2, Pin.OUT)
	relay = led
	# buzzer = PWM(Pin(2))
	# pwm.duty(512)
else:
	def relay(state):
		if state:
			temp_event.set(temp_event.value() + mypid.output)
		print('relay {}'.format(state))


async def heater(timer_event):
	while True:
		await timer_event	
		print('==start heating==')	
		while timer_event.is_set():	
			time = timer_event.value()
			setpoint = setpoint_event.value()
			temp = temp_event.value()

			if time > 0:
				timer_event.set(time - RELAY_CICLE_SEC)
				print('time_lost = {} setpoint = {}'.format(time, setpoint))
				

				mypid.SetPoint = setpoint
				mypid.update(temp)
				u = mypid.output
				if u < 0:
					u = 0
				if u > RELAY_CICLE_SEC:
					u = RELAY_CICLE_SEC
				print('u = {} last_error={}'.format(u, mypid.last_error))
				relay(1)
				await asyncio.sleep(u) 
				relay(0)
				await asyncio.sleep(RELAY_CICLE_SEC - u)
			else:
				timer_event.clear()
				setpoint_event.clear()
				print('==stop heating==')

async def sensor():
	i=1
	while True:
		await asyncio.sleep(1)
		# volume = adc.read()
		# temperature = termistor(volume)
		# temperature = int(100 * math.sin(i/360))
		# i += 1

		print('temperature = {}'.format(temp_event.value()))
