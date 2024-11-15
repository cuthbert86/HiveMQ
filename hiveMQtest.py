import paho.mqtt.client as mqtt
import time
#from sense_hat import SenseHat
import json
from hive_settngs import BROKER, PORT, USERNAME, PASSWORD, TOPIC
#sense = SenseHat()
# The callback function. It will be triggered when trying to connect to the MQTT broker
# client is the client instance connected this time
# userdata is users' information, usually empty. If it is needed, you can set it through user_data_set function.
# flags save the dictionary of broker response flag.
# rc is the response code.
# Generally, we only need to pay attention to whether the response code is 0.


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to HiveMQ!")
        # Subscribe to the topic
        client.subscribe(TOPIC)
    else:
        print(f"Connection failed with code {rc}")


def on_message(client, userdata, msg):
    print(f"Received message: '{msg.payload.decode()}' on topic '{msg.topic}'")


# Callback function when a message is published
def on_publish(client, userdata, mid):
    print("Message published successfully")


client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()  # Enable SSL/TLS

client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Connect to the HiveMQ broker
client.connect(BROKER, PORT)

# Start the client loop
client.loop_start()

# Publish messages to the topic
try:
    for i in range(5):  # Publish 5 messages
        message = f"Hello HiveMQ! Message {i+1}"
        result = client.publish(TOPIC, message)
        result.wait_for_publish()  # Wait until the message is published
        time.sleep(1)  # Delay between messages
except KeyboardInterrupt:
    print("Publishing stopped")

# Keep the subscription active for some time
time.sleep(10)  # Adjust time as needed
client.loop_stop()
client.disconnect()
