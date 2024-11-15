import paho.mqtt.client as mqtt
import json
import time
from sense_hat import SenseHat
from datetime import datetime
from collections import deque
# from array import *
import numpy as np
import pandas
import sqlite3
import csv
from csv import writer, reader, DictWriter
# from statistics import mean

# CSV file path
csvfile = "store2.csv"
sense = SenseHat()
json_string = '{"temp": "36.24469757080078", "Humidity": "37.37043380737305", "Date": "2024-03-22 00:13:27.122036"}'
data1 = json.loads(json_string)
# Initialize deque with 120 None values
data_window = deque([], maxlen=120)
data_week = deque([], maxlen=840)
data_month = deque([], maxlen=3360)


# Now you can access the data fields individually
temperature = float()
humidity = float()
date = data1["Date"]
day = float()
week = float()
month = float()



# MQTT broker details
broker_address = "localhost"  # Use the address of your local MQTT broker
port = 1883                 # Default MQTT port
temp1 = float()
# Create an MQTT client instance
client = mqtt.Client("csv_publisher")
conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   temperature REAL,
                   humidity REAL,
                   pressure REAL,
                   timestamp TEXT)''')
# Connect to the MQTT broker
client.connect(broker_address, port)
cursor = conn.cursor()
# Define the topic to which you want to publish
topic = "data1"

start_time = time.time()
duration = 400


def write_to_csv(file_name, var1, var2, var3, var4):
    # Open the CSV file in append mode
    with open(file_name, 'a', newline='') as csvfile:
        # Create a CSV writer object
        writer1 = csv.writer(csvfile)
        # Write the variables as a single line
        writer1.writerow([var1, var2, var3, var4])
    # Read the data point from the CSV file


def calculate_rolling_averagemean(data):
    total = sum(data)
    num1 = len(data)
    aveMean = total / num1
#   ave1 = mean([data_window])
#   print(ave)
    return aveMean


# Run the while loop for the specified duration
while (time.time() - start_time) < duration:
    data_window.appendleft(sense.get_temperature())
    data_week.appendleft(sense.get_temperature())
    data_month.appendleft(sense.get_temperature())
    data1 = {"temp": str(sense.get_temperature()),
             "Humidity": str(sense.get_humidity()),
             "Date": str(datetime.now().isoformat()),
             "Ave1": str(calculate_rolling_averagemean(data_window)),
             "AveWeek": str(calculate_rolling_averagemean(data_week)),
             "AveMonth": str(calculate_rolling_averagemean(data_month)),
             }

    # Collect sensor data
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()
    timestamp = datetime.now().isoformat()
    write_to_csv(csvfile, temperature, humidity, pressure, timestamp)
    # Insert data into the table
    cursor.execute('''INSERT INTO sensor_data (temperature, humidity, pressure, timestamp)
                      VALUES (?, ?, ?, ?)''', (temperature, humidity, pressure, timestamp))

    # Commit changes to the database
    conn.commit()

    print("Saved sensor data:", temperature, humidity, pressure, timestamp)

# Convert dictionary to JSON string
    message = json.dumps(data1)
    ave2 = calculate_rolling_averagemean(data_week)
# print(ave2)
    ave3 = calculate_rolling_averagemean(data_month)
# print (ave3)
    client.publish(topic, message)
    print(f"Published: {message} to topic: {topic}")
# Sleep for a short duration if needed
    time.sleep(3)

    rolling_avg = calculate_rolling_averagemean(data_window)
    print(f"Calculted Rolling averages: {data1}")
# Disconnect from the MQTT broker
else:
    client.disconnect()
