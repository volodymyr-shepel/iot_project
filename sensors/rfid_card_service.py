import RPi.GPIO as GPIO
from mfrc522 import MFRC522
import signal
import time
import MqttPublisher

class MFRC522Reader:
    def __init__(self,mqtt_publisher,id):
        self.id = id
        self.MIFAREReader = MFRC522()
        self.continue_reading = True
        self.mqtt_publisher = mqtt_publisher
        # Welcome message
        print("Welcome to the MFRC522 data read example")
        print("Press Ctrl-C to stop.")

        # Hook the SIGINT
        signal.signal(signal.SIGINT, self.end_read)
    # the method which is called when user clicks Ctrl-C
    def end_read(self, signal, frame):
        self.continue_reading = False
        GPIO.cleanup()
        print("Ctrl+C captured, ending read.")


    # method is responsible for authenticating and reading a specific memory block from an RFID card.
    def read_mifare_block(self, key, uid, blockAddr):
        # Authenticate
        status = self.MIFAREReader.MFRC522_Auth(self.MIFAREReader.PICC_AUTHENT1A, blockAddr, key, uid)
        
        # Check if authenticated
        if not(status == self.MIFAREReader.MI_OK):
            print("Authentication error for block {}".format(blockAddr))
            return (status, [])

        recvData = []
        recvData.append(self.MIFAREReader.PICC_READ)
        recvData.append(blockAddr)
        pOut = self.MIFAREReader.CalulateCRC(recvData)
        recvData.append(pOut[0])
        recvData.append(pOut[1])
        (status, backData, backLen) = self.MIFAREReader.MFRC522_ToCard(self.MIFAREReader.PCD_TRANSCEIVE, recvData)
        
        if not(status == self.MIFAREReader.MI_OK):
            return (status, [])
        return (status, backData)

    # In RFID card systems, data is often organized into blocks, and the dump_card method reads and displays the content of each 
    # block of the card's memory.
    def dump_card(self, key, uid):
        # Select the scanned tag
        self.MIFAREReader.MFRC522_SelectTag(uid)

        for block in range(64):
            (status, mem) = self.read_mifare_block(key, uid, block)
            if status == self.MIFAREReader.MI_OK:
                print("Block {:2d} [{:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x} {:02x}]".format(
                    block, mem[0], mem[1], mem[2], mem[3], mem[4], mem[5], mem[6], mem[7], mem[8], mem[9], mem[10], mem[11], mem[12], mem[13], mem[14], mem[15]))
            else:
                print("Read error for block {}".format(block))

        self.MIFAREReader.MFRC522_StopCrypto1()
        print("Card memory read end")


    def read_card(self):
        # Scan for cards
        (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == self.MIFAREReader.MI_OK:
            print("Card detected")

        # Get the UID of the card
        (status, uid) = self.MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == self.MIFAREReader.MI_OK:
            # Print UID
            # Extract UID components
            # [2:] is needed because each block starts with 0x so we do not need it
            # P.S change if cards will return different uid
            uid_block_1 = hex(uid[0])[2:]
            uid_block_2 = hex(uid[1])[2:]
            uid_block_3 = hex(uid[2])[2:]
            uid_block_4 = hex(uid[3])[2:]

            # Create a formatted string with hyphens which will be sent to the server and it will verify access based on it
            # There is a db where uid is primary key and it contains information who is an owner,rights etc.
            formatted_uid = "{}-{}-{}-{}".format(uid_block_1, uid_block_2, uid_block_3, uid_block_4)

            # used to publish the id of the card to message queue(sent to brocker)
            # formatted_uid represents the measurement
            self.mqtt_publisher.publish_measurement(measurement = formatted_uid,id = self.id)
            
            # This is the default key for authentication
            #key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

            # used to read the content of the card
            # TODO: uncomment if needed to read the content
            #self.dump_card(key, uid)
