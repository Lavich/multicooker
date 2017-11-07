import uasyncio as asyncio
from asyn import Event
# from machine import ADC, Pin

setpoint_event = Event()
relay_event = Event()
heater_event = Event()
start_event = Event()
temperature = 0
RELAY_CICLE_SEC = 10

# adc = ADC(0)
# relay = Pin()

async def sensor():
	i=0
	while True:
		await asyncio.sleep(1)
		# volume = adc.read()
		# temperature = termistor(volume)	
		i += 1
		print('def sensor({})'.format(i))

async def start(start_event):
	while True:
		await start_event
		print('def start()')
		data = start_event.value()
		temp = int(data['temp'])
		time = int(data['time'])
		await set_heater(temp, time)
		start_event.clear()

async def set_heater(setpoint, time):
	print('def set_heater(setpoint={}, time={})'.format(setpoint, time))
	heater_event.set(setpoint)
	await asyncio.sleep(time)
	heater_event.clear()
	return 0

async def heater(setpoint):
	while True:
		await heater_event
		while heater_event.is_set():
			print('def heater()')
			# u = pid(heater_event.value(), temperature)
			u = 0.5
			relay_event.set(u)
			await asyncio.sleep(RELAY_CICLE_SEC)
		relay_event.clear()
		
async def relay(relay_event):
	while True:
		await relay_event
		while relay_event.is_set():
			print('def relay()')
			relay_on = relay_event.value() * RELAY_CICLE_SEC
			relay_off = RELAY_CICLE_SEC - relay_on
			# relay.higth()
			print('relay ON')
			await asyncio.sleep(relay_on)
			print('relay OFF')
			# relay.low()
			await asyncio.sleep(relay_off)
		print('relay OFF')

