import traceback
import config
import RPi.GPIO as GPIO
import time
from MqttPublisher import MqttPublisher
from MqttSubscriber import MqttSubscriber
import server_mqtt_service

# for database sqlite will be used
def main():

    access_checker = server_mqtt_service.AccessChecker()
        # used to accept the result from server
    sensors_subscriber = MqttSubscriber("sensors","server_subscriber",access_checker.check_access)
    sensors_subscriber.connect()

    try:
        while True:
            pass
           
    except KeyboardInterrupt:
        print ('\r\ntraceback.format_exc():\n%s' % traceback.format_exc())
        GPIO.cleanup()
        config.module_exit()
        exit()

if __name__ == "__main__":
    main()