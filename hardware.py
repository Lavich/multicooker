import sys
import utime
import uasyncio
from asyn import Event

import math
import uasyncio as asyncio

from models import Step

NOMINAL_T = 25
THERMISTOR_R = 100000
SERIAL_R = 120000
B = 3950


recipe_event = Event()
setpoint_event = Event()
relay_event = Event()

def termistor(adc):
    resistor = SERIAL_R / (1023 / adc - 1)
    temperature = 1 / (math.log(resistor / THERMISTOR_R) / B + 1 / (NOMINAL_T + 273.15)) - 273.15
    return temperature


if sys.platform == 'esp8266':
	from machine import ADC, Pin
	adc = ADC(0)
	relay = Pin(2, Pin.OUT)
	def termistor():
		volume = adc.read()
		temperature = volume
		return temperature
else:
	import math
	relay = lambda x: print('Relay is {}'.format(x))
	termistor = math.sin(utime.time()/90)

mediana_list = 7*[0]

def mediana(temp):
	mediana_list.pop(0)
	mediana_list.append(temp)
	temp = sorted(mediana_list)[3]
	return temp

def pid(setpoint):
	pass
	return 0

async def start(recipe_event):
    while True:
        await recipe_event
        steps = list(Step.filter(recipe_name=recipe_event.value()))
        recipe_event.clear()
        for step in steps:
        	print('Recipe={} Step_id={}'.format(step['recipe_name'], step['id']))
        	setpoint_event.set(step)


async def measure_temp():
    while True:
    	temp = 10
    	temp = mediana(temp)
    	
        await asyncio.sleep(2)

async def relay(relay_event):
    while True:
        await relay_event
        while relay_event.is_set():
            print('relay ON')
            await asyncio.sleep_ms(1000)
	
async def pid(setpoint_event, relay_event):
    while True:
    	await setpoint_event
        while setpoint_event.is_set():
            id = setpoint_event.value()['id']
            time = setpoint_event.value()['time']
            setpoint = setpoint_event.value()['temperature']
            relay_event.set(setpoint)
            print('id={} time={} temp={}'.format(id, time, setpoint))
            await asyncio.sleep(int(time))
        relay_event.clear()

async def run():
    loop = asyncio.get_event_loop()

    loop.create_task(measure_temp())
    loop.create_task(relay(relay_event))
    loop.create_task(start(recipe_event))
    loop.create_task(pid(setpoint_event, relay_event))
