import json
import time
import paho.mqtt.client as mqtt			# importing mqtt library
from datetime import datetime
import sqlite3

class MqttClient:
    
    publishers = {}
    BROKER_HOST="10.108.33.121" # address of server raspberry pi					
    PORT=1883

    def __init__(self, topic_pub, topic_sub, client_name, on_receive_message):
        self.topic_pub = topic_pub # TODO: specify the topic to which publish
        
        self.topic_sub = topic_sub # TODO: specify the topic to which publish
        self.client_name = client_name
        self.connected_flag = False
        self.client = mqtt.Client(client_name)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.on_receive_message = on_receive_message
 
    def publish_measurement(self, measurement, id):
        # publish it like a json so i can identify the sensor
        message = {"id": id, "measurement": measurement}
        json_message = json.dumps(message)
        
        print(f"{self.topic_pub}: {json_message}")
        self.client.publish(f"{self.topic_pub}/{id}", json_message, 0, True)
#/topic/id/
    def on_message(self, client, userdata, msg):
        now = datetime.now().time()
        payload = msg.payload.decode("utf-8")

        print("Msg received {}, topic: {} value: {}".format(now, msg.topic, payload))

        message_data = json.loads(payload)
        room_id = message_data.get("id")

        result = self.on_receive_message(message_data)
        
        # Reuse existing publisher or create a new one if not present
        # if room_id in self.publishers:
        #     room_publisher = self.publishers[room_id]
        # else:
        #     room_publisher = self.publish_measurement()
        #     room_publisher = MqttPublisher(f"ROOM{room_id}", f"room{room_id}_sensor")
        #     room_publisher.connect()
        #     self.publishers[room_id] = room_publisher

        self.publish_measurement(result, room_id)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            client.connected_flag = True
            print("Connected OK")
            
            # conn = sqlite3.connect('attendance_system.db')
            # cursor = conn.cursor()

            # # Retrieve all room IDs from the Room table
            # cursor.execute("SELECT room_id FROM Room")
            # room_ids = cursor.fetchall()

            # # Parse room IDs into a list
            # room_ids_list = [row[0] for row in room_ids]
            
            # print("Room IDs:", room_ids_list)
            
            # for room in room_ids_list:
            client.subscribe(f"{self.topic_sub}", qos=0)
            # Print the result
            ##TODO connect to several topic through list
            
        else:
            print("Bad connection Returned code=", rc)

    def connect(self):
        #self.client.username_pw_set(self.USER, password=self.KEY)
        self.client.connect(self.BROKER_HOST, port=self.PORT, keepalive=60)
        self.client.loop_start()

    def disconnect(self):
        self.publishers = {}
        self.client.loop_stop()
        self.client.disconnect()