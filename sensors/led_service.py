import board
import neopixel 
import time

#Msg received 13:55:30.461652, topic: r0gue/feeds/LEDBTN1 value: ON
#Msg received 13:55:43.324076, topic: r0gue/feeds/LED1 value: #ffffff

class LedService:
    color = (255,0,0)

    success_color = (0,255,0)
    fail_color = (255,0,0)
    status = "OFF"

    def __init__(self):
        self.ledStrip = neopixel.NeoPixel(
                        board.D18,
                        8,
                        brightness=1.0/32,
                        auto_write=False)
    
    def light_led(self, color,index):
    # Convert hex color string to RGB
        hex_color = color.lstrip('#')
        red = int(hex_color[0:2], 16)
        green = int(hex_color[2:4], 16)
        blue = int(hex_color[4:6], 16)

        self.color = (red, green, blue)

        if self.status == "ON":
            self.ledStrip[index -1] = (red, green, blue)
            
            self.ledStrip.show()
    
    
    def change_led_status(self,status,index):
        print(f'Is on {status == "ON"}')
        print(f'Is off {status == "OFF"}')
        if status == "ON":
            self.status = "ON"
            self.ledStrip[index -1] = self.color
        elif status == "OFF":
            self.status = "OFF"
            self.ledStrip[index -1] = (0,0,0)
        self.ledStrip.show()
    
    def lightStrip(self,color):
        self.ledStrip.fill(color)
        self.ledStrip.show()
        time.sleep(2)
        self.ledStrip.fill((0,0,0))
        self.ledStrip.show()
    

    def blink_led(self,msg):
        payload = msg.payload.decode("utf-8")

        if payload == 'True': # open the door
            self.lightStrip(self.success_color)
        else:
            self.lightStrip(self.fail_color)
        

