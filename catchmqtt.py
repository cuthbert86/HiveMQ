# This program works but it requires paho-mqtt to be installed (which was more difficult than it should have been, probably because i was on a windows laptop)
import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
from collections import deque
from hive_settngs import BROKER, PORT, USERNAME, PASSWORD, TOPIC
# from array import *
# import numpy as np
# import pandas
import sqlite3
import csv
from csv import writer, reader, DictWriter
# The callback function. It will be triggered when trying to connect to the MQTT broker
# client is the client instance connected this time
# userdata is users' information, usually empty. If it is needed, you can set it through user_data_set function.
# flags save the dictionary of broker response flag.
# rc is the response code.
# Generally, we only need to pay attention to whether the response code is 0.
csvfile = "store2.csv"
json_string = '{"temp": "36.24469757080078", "Humidity": "37.37043380737305", "Date": "2024-03-22 00:13:27.122036"}'
data1 = json.loads(json_string)
temp = float()
temp1 = float()
temperature = float()
humidity = float()
humidity1 = float()
date = data1["Date"]
timestamp = datetime.now().isoformat()
day = float()
week = float()
month = float()
data_window = deque([], maxlen=120)
data_week = deque([], maxlen=840)
data_month = deque([], maxlen=3360)

conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   temperature REAL,
                   humidity REAL,
                   timestamp TEXT)''')


cursor = conn.cursor()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to HiveMQ!")
        # Subscribe to the topic
        client.subscribe(TOPIC)
    else:
        print(f"Connection failed with code {rc}")


# Callback function when a message is published
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    time.sleep(4)
    print("Subscribed: ")


def write_to_csv(file_name, var1, var2, var3, var4, var5, var6):
    # Open the CSV file in append mode
    with open(file_name, 'a', newline='') as csvfile:
        # Create a CSV writer object
        writer1 = csv.writer(csvfile)
        # Write the variables as a single line
        writer1.writerow([var1, var2, var3, var4, var5, var6])
    # Read the data point from the CSV file


def calculate_rolling_averagemean(data):
    total = sum(data)
    num1 = len(data)
    aveMean = total / num1
#   ave1 = mean([data_window])
#   print(ave)
    return aveMean


def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")
    try:
        jstring = str(msg.payload.decode("utf-8","ignore"))
        print(jstring)
        process_json(jstring)
        time.sleep(2)
        return (data_window, data_week, data_month)
    except:
        print("oops")


def process_json(d1):
    data = json.loads(d1)
    temp = float(data["temp"])
    temp1 = truncate_float(temp)
    humidity = float(data["Humidity"])
    humidity1 = truncate_float(humidity)
    timestamp = data["Date"]
    print("Temperature:", temp1)
    print("Humidity:", humidity1)
    print("Timestamp:", timestamp)
    data_window.appendleft(temp1)
    data_week.appendleft(temp1)
    data_month.appendleft(temp1)
    temp_ave2 = calculate_rolling_averagemean(data_week)
    ave2 = truncate_float(temp_ave2)
    temp_ave3 = calculate_rolling_averagemean(data_month)
    ave3 = truncate_float(temp_ave3)
    temp_rolling_avg = calculate_rolling_averagemean(data_window)
    rolling_avg = truncate_float(temp_rolling_avg)
    print(f"{ave2},{ave3},{rolling_avg}")
    write_to_csv(csvfile, temp1, humidity1, timestamp, rolling_avg,
                 ave2, ave3)
    cursor.execute('''INSERT INTO sensor_data (temperature, humidity,
                       timestamp)
                      VALUES (?, ?, ?)''', (temp1, humidity1,
                                            timestamp))
# Commit changes to the database
    conn.commit()
    return (temp1, humidity1, timestamp, ave2, ave3, rolling_avg)


def truncate_float(value, digits_after_point=2):
    pow_10 = 10 ** digits_after_point
    return (float(int(value * pow_10))) / pow_10


client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()  # Enable SSL/TLS
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
# Connect to the HiveMQ broker
client.connect(BROKER, PORT)
start_time = time.time()
duration = 4000
while (time.time() - start_time) < duration:
    client.loop_start()
    client.subscribe(TOPIC)
    time.sleep(3)
    client.loop_forever
# Set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.disconnect()
