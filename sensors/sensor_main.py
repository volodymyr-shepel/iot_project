import traceback
import config
import RPi.GPIO as GPIO
import time
from MqttPublisher import MqttPublisher
from MqttSubscriber import MqttSubscriber
import rfid_card_service
import led_service


def main():

    # specifies where to publish
    room_1_card_sensor_publisher = MqttPublisher("sensors","room1_sensor") 
    
    room_1_card_sensor_publisher.connect()

    # specifies how to read the data from the card and publishes the result
    rfid_card_service_room_1 = rfid_card_service.MFRC522Reader(room_1_card_sensor_publisher,1)

    # each sensor has separate mq(subscribe to accept messages)
    # but all sensors publish to the same message queue
    
    # used to accept the result from server
    room_1_sensor = MqttSubscriber("ROOM1","room1_sensor",led_service.blink_led)
    room_1_sensor.connect()

    try:
        while True:
            rfid_card_service_room_1.read_card()
            time.sleep(0.5)
           
    except KeyboardInterrupt:
        print ('\r\ntraceback.format_exc():\n%s' % traceback.format_exc())
        GPIO.cleanup()
        config.module_exit()
        exit()

if __name__ == "__main__":
    main()