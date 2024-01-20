import paho.mqtt.client as mqtt			# importing mqtt library
from datetime import datetime

class MqttSubscriber:

    BROKER_HOST="io.adafruit.com" # address of server raspberry pi					
    PORT=1883
    USER="r0gue" # user ! change when security will be set up
    KEY="aio_DwSR74zv1N0QoTNIbSTjTFZohHq7" # key ! change when security will be set up

    # on_receive message is a method which will be invoked when the message is received
    def __init__(self, topic, client_name,on_receive_message):
        self.topic = f'{self.USER}/feeds/{topic}' # TODO: change topic accordingly
        self.client_name = client_name
        self.client = mqtt.Client(client_name)
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.on_receive_message = on_receive_message


    def on_message(self,client, userdata, msg):
        now = datetime.now().time()
        payload = msg.payload.decode("utf-8")
        
        
        print("Msg received {}, topic: {} value: {}".format(now, msg.topic, payload))
        self.on_receive_message(msg) # pass message not payload so I can extract more information and make it more general
    
    def on_connect(self,client, userdata, flags, rc):		# function called on connected
        if rc==0:
            client.connected_flag=True 			# set flag
            print("Connected OK")
            client.subscribe(f"{self.USER}/errors", qos=0)
            client.subscribe(self.topic, qos=0)
        else:
            print("Bad connection Returned code=",rc)

    def connect(self):
        self.client.username_pw_set(self.USER, password=self.KEY)
        self.client.connect(self.BROKER_HOST, port=self.PORT,keepalive=60)
        self.client.loop_start()
    
