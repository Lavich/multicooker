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


start_event = Event()
step_event = Event()
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
	return 0.5



async def measure_temp():
    """
    Measure temperature in AO
    """
    while True:
        temp = 10
        temp = mediana(temp)   	
        await asyncio.sleep(1)


async def start(start_event):
    """
	Start function
	"""
    while True:
        await start_event
        steps = list(Step.filter(recipe_name=start_event.value()))
        start_event.clear()
        for step in steps:
            print('Recipe={} Step_id={} time={}s'.format(step['recipe_name'], step['id'], step['time']))
            step_event.set(int(step['temperature']))
            await asyncio.sleep(int(step['time']))


async def step(step_event):
    while True:
        await step_event
        while step_event.is_set():
            setpoint = step_event.value()
            u = pid(setpoint)
            relay_event.set(u)
            print('def step: setpoint={}'.format(setpoint))
            await asyncio.sleep_ms(1000)


async def relay(relay_event):
    while True:
        await relay_event
        while relay_event.is_set():
            time_on = int(relay_event.value()) * 1000
            time_off = 1000 - time_on
            print('relay ON')
            await asyncio.sleep_ms(time_on)
            print('relay OFF')
            await asyncio.sleep_ms(time_off)


async def run():
    loop = asyncio.get_event_loop()

    loop.create_task(measure_temp())
    loop.create_task(relay(relay_event))
    loop.create_task(start(start_event))
    loop.create_task(step(step_event))
