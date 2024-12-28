# To install packages with micropython go into the thonny command line and type import mip
# then type mip.install("umqtt.simple.py")   or whatever libarary you wan tto install.  
# as far as i know upip is basically obselete 

import network
import usocket
from time import time, sleep
import network
import time
from umqtt.simple import MQTTClient
import machine
from picozero import pico_temp_sensor
from machine import Pin
import micropython
import ustruct as struct
import json
import network
import time
import random

adcpin = 4
sensor = machine.ADC(adcpin)
sock = usocket
SSID = 'BB'
WIFI_PASSWORD = b'6KH1jk1mn0s'
# SERVER_HOSTNAME = "e5d2174059b64286bd5f243dd055355a.s1.eu.hivemq.cloud:8884/mqtt"

USER = "Cuthbert"
wlan = network.WLAN(network.STA_IF)
broker_address = "localhost"
adcpin = 4
sensor = machine.ADC(adcpin)
sock = usocket
SSID = ****
PASSWORD = ******
#SERVER_HOSTNAME = "e5d2174059b64286bd5f243dd055355a.s1.eu.hivemq.cloud:8884/mqtt"
USER = "Cuthbert"
TOPIC = "test_data"
wlan = network.WLAN(network.STA_IF)
mqtt = MQTTClient
#sending = broker_address
BROKER = "192.168.1.11"
PORT = "1887"  # Topic to publish to
CLIENT_ID = "Cuthbert"


def ReadTemperature():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    temp = str(round(temperature, 1))
    print(temp)
    return temp

# Replace with your Wi-Fi password
def connect_to_wifi():
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(1)
        print("Waiting for connection...")
    else:
        print("Wi-Fi connected!")
        print("IP address:", wlan.ifconfig())


def sensor_data_to_json(temperature):

    # Create a dictionary to hold the sensor data
    sensor_data = {
        "temperature": temperature,
    }

    # Convert the dictionary to a JSON string
    json_data = json.dumps(sensor_data)
    return json_data

Temperature = ReadTemperature()
json_string = '{"temp":"27"}'
data1 = json.loads(json_string)



# Publish data

connect_to_wifi()
client = MQTTClient(CLIENT_ID, BROKER)

try:
    print("Connecting to MQTT broker...")
    client.connect()
    print("Connected to MQTT broker.")

    while True:
        Temperature = ReadTemperature()
        json_result = sensor_data_to_json(Temperature)
        print (json_result)
        client.publish(TOPIC, json_result)
        time.sleep(5)  # Publish every 5 seconds
        Temperature = ReadTemperature()
        json_result = sensor_data_to_json(Temperature)
        print(json_result)
        client.publish(TOPIC, json_result)
        time.sleep(5)
        Temperature = ReadTemperature()
        json_result = sensor_data_to_json(Temperature)
        print (json_result)
        client.publish(TOPIC, json_result)
        Temperature = ReadTemperature()
        json_result = sensor_data_to_json(Temperature)
        print (json_result)
        client.publish(TOPIC, json_result)
        
except Exception as e:
    print("An error occurred:", e)
    
