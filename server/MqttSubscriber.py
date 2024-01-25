# import paho.mqtt.client as mqtt
# from datetime import datetime
# import json

# from server.MqttPublisher import MqttPublisher

# class MqttSubscriber:

#     publishers = {}
#     BROKER_HOST = "io.adafruit.com"
#     PORT = 1883
#     #USER="r0gue" # user ! change when security will be set up
#     #KEY="aio_DwSR74zv1N0QoTNIbSTjTFZohHq7" # key ! change when security will be set up

#     def __init__(self, topic, client_name, on_receive_message):
#         self.topic = topic
#         self.client_name = client_name
#         self.client = mqtt.Client(client_name)
#         self.client.on_message = self.on_message
#         self.client.on_connect = self.on_connect
#         self.on_receive_message = on_receive_message

#     def on_message(self, client, userdata, msg):
#         now = datetime.now().time()
#         payload = msg.payload.decode("utf-8")

#         print("Msg received {}, topic: {} value: {}".format(now, msg.topic, payload))

#         message_data = json.loads(payload)
#         room_id = message_data.get("id")

#         result = self.on_receive_message(msg)
        
#         # Reuse existing publisher or create a new one if not present
#         if room_id in self.publishers:
#             room_publisher = self.publishers[room_id]
#         else:
#             room_publisher = MqttPublisher(f"ROOM{room_id}", f"room{room_id}_sensor")
#             room_publisher.connect()
#             self.publishers[room_id] = room_publisher

#         room_publisher.publish_measurement(result)

#     def on_connect(self, client, userdata, flags, rc):
#         if rc == 0:
#             client.connected_flag = True
#             print("Connected OK")
#             client.subscribe(self.topic, qos=0)
#         else:
#             print("Bad connection Returned code=", rc)

#     def connect(self):
#         #self.client.username_pw_set(self.USER, password=self.KEY)
#         self.client.connect(self.BROKER_HOST, port=self.PORT, keepalive=60)
#         self.client.loop_start()

#     def disconnect(self):
#         for room_id, room_publisher in self.publishers.items():
#             room_publisher.stop()
#         self.publishers = {}
#         self.client.loop_stop()
#         self.client.disconnect()
