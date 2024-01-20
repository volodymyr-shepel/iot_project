import paho.mqtt.client as mqtt
import time

class MqttPublisher:

    BROKER_HOST="io.adafruit.com" # ip address of another raspberry pi				
    PORT=1883
    user="r0gue" # user  ! change when security will be set up
    key="aio_DwSR74zv1N0QoTNIbSTjTFZohHq7" # key ! change when security will be set up

    # topic is where to publish
    def __init__(self, topic, client_name,id):
        self.id = id
        self.topic = topic # TODO: specify the topic to which publish
        self.client_name = client_name
        self.connected_flag = False
        self.client = mqtt.Client(client_name)
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected_flag = True
            print(f"Connected OK.{self.client_name}")
        else:
            print("Bad connection. Returned code=", rc)

    def connect(self):
        self.client.username_pw_set(self.user, password=self.key)
        self.client.connect(self.BROKER_HOST, port=self.PORT)
        self.client.loop_start()

        while not self.connected_flag:
            print("Waiting for connection")
            time.sleep(1)

    def publish_measurement(self,measurement):
        print(f"{self.topic}: {measurement}")
        self.client.publish(self.topic, measurement, 0, True)
    
    def stop(self):
        self.client.loop_stop()    				
        self.client.disconnect()
