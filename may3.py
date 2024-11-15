import paho.mqtt.client as mqtt
import json
import time
from sense_hat import SenseHat
from datetime import datetime
from collections import deque
import csv
# import pandas as pd
# from pandas import DataFrame as df
# from csv import writer, DictWriter
# from array import *
# import numpy as np
# from statistics import mean

csvfile = "store2.csv"
sense = SenseHat()
# Initialize deque with 120 None values
data_window = deque([], maxlen=120)
data_week = deque([], maxlen=600)
data_month = deque([], maxlen=1200)
# These are a special type of array that enables the storage of data to be used for staticial calculations later.
# MQTT broker details
broker_address = "localhost"  # Use the address of your local MQTT broker
port = 1883       # Default MQTT port
temp1 = float()
# Create an MQTT client instance
client = mqtt.Client()
warning = json.dumps({
    "Warning": str("WARNING! Overheating!")
    })
# Connect to the MQTT broker
client.connect(broker_address, port)
# Define the topic to which you want to publish
topic = "test_data"
# topic2 = "t2"lolo
# topic3 = "t3"
# topic4 = "t4"
# topic5 = "t5"
start_time = time.time()
duration = 50000


def write_to_csv(file_name, var1, var2, var3, var4):
    # Open the CSV file in append mode
    with open(file_name, 'a', newline='') as csvfile:
        # Create a CSV writer object
        writer1 = csv.writer(csvfile)
        # Write the variables as a single line
        writer1.writerow([var1, var2, var3, var4])
# This saves the data to a correctly formatted CSV file


def calculate_rolling_averagemean(data):
    total = sum(data)
    num1 = len(data)
    aveMean = total / num1
#   ave1 = mean([data_window])
#   print(ave)
    return aveMean
# This calculates the rolling average


def truncate_float(value, digits_after_point=4):
    pow_10 = 10 ** digits_after_point
    return (float(int(value * pow_10))) / pow_10
# this limits the number of decimal places used.


# Run the while loop for the specified duration
while (time.time() - start_time) < duration:
    temp = truncate_float(sense.get_temperature())
    humidity = truncate_float(sense.get_humidity())
    pressure = truncate_float(sense.get_pressure())
    timestamp = datetime.now().isoformat()
# this creates a correctly formatted "datetime" variable.
    data_window.appendleft(temp)
    data_week.appendleft(temp)
    data_month.appendleft(temp)
    rolling_avg = truncate_float(calculate_rolling_averagemean(data_window))
    ave2 = truncate_float(calculate_rolling_averagemean(data_week))
    ave3 = truncate_float(calculate_rolling_averagemean(data_month))
    message = json.dumps({"temp": (float(temp)),
             "Humidity": (float(humidity)),
             "Pressure": (float(pressure)),
             "Date": (datetime.now().isoformat()),
             "Ave1": (float(rolling_avg)),
             "AveWeek": (float(ave2)),
             "AveMonth": (float(ave3))
             })
    client.publish(topic, message)
#    client.publish(topic, message)
  #  client.publish(topic3, message)
  #  client.publish(topic4, message)
  #  client.publish(topic5, message)
    print(f"Published: {message} to topic: {topic}")
# Sleep for a short duration if needed
    time.sleep(10)
    write_to_csv(csvfile, temp, humidity, pressure, timestamp)
    print(f"Calculted Rolling averages: {message}")
    difference = abs(temp - rolling_avg)
    threshold = 0.1 * rolling_avg
    if difference > threshold:
        client.publish(topic, warning)
        print(warning)  # this gives a Warning if there is a new data point over 10% different to the average
    else:
        pass

# Disconnect from the MQTT broker
else:
    client.disconnect()
