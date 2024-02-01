import json
import time
import paho.mqtt.client as mqtt			# importing mqtt library
from datetime import datetime


class MqttClient:
    BROKER_HOST="10.108.33.121" # address of server raspberry pi					
    PORT=8883

    def __init__(self, topic_pub, topic_sub, client_name, on_receive_message):
        self.topic_pub = topic_pub # TODO: specify the topic to which publish
        self.topic_sub = topic_sub # TODO: specify the topic to which publish
        self.client_name = client_name
        self.connected_flag = False
        self.client = mqtt.Client(client_name)
        self.client.tls_set(ca_certs="../certs/ca/crt",
                            cert_reqs=mqtt.ssl.CERT_NONE,
                            tls_version=mqtt.ssl.PROTOCOL_TLSv1_2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.on_receive_message = on_receive_message
 
    def on_message(self,client, userdata, msg):
        now = datetime.now().time()
        payload = msg.payload.decode("utf-8")
        
        print("Msg received {}, topic: {} value: {}".format(now, msg.topic, payload))
        self.on_receive_message(msg) # pass message not payload so I can extract more information and make it more general
    
    def on_connect(self,client, userdata, flags, rc):		# function called on connected
        if rc==0:
            self.connected_flag = True
            client.subscribe(self.topic_sub, qos=0)
            print(f"Connected OK.{self.client_name}")
        else:
            print("Bad connection Returned code=", rc)

    def publish_measurement(self, measurement, id):
        # publish it like a json so i can identify the sensor
        message = {"id": id, "measurement": measurement}
        print(message)
        json_message = json.dumps(message)
        
        print(f"{self.topic_pub}: {json_message}")
        self.client.publish(self.topic_pub, json_message, 0, True)
    
    def connect(self):
        # TODO : uncomment when set security
        #self.client.username_pw_set(self.USER, password=self.KEY)
        self.client.connect(self.BROKER_HOST, port=self.PORT,keepalive=60)
        self.client.loop_start()

        while not self.connected_flag:
            print("Waiting for connection")
            time.sleep(1)
    
    def stop(self):
        self.client.loop_stop()    				
        self.client.disconnect()
    
