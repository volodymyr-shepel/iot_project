from datetime import datetime
import busio
import board
import adafruit_bme280.advanced as adafruit_bme280
import requests
from bs4 import BeautifulSoup

class SensorService:
    def __init__(self):
        # Sensor variables definition
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(self.i2c, 0x76)

        # Setup sensor parameters
        self.bme280.mode = adafruit_bme280.MODE_NORMAL
        self.bme280.standby_period = adafruit_bme280.STANDBY_TC_500
        self.bme280.iir_filter = adafruit_bme280.IIR_FILTER_X16
        self.bme280.overscan_pressure = adafruit_bme280.OVERSCAN_X16
        self.bme280.overscan_humidity = adafruit_bme280.OVERSCAN_X1
        self.bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2

    
    def calculate_altitude(self, sea_level_pressure):
        adafruit_bme280.sea_level_pressure = sea_level_pressure
        return adafruit_bme280.altitude
    
    def get_sea_level_pressure(self):
        url = 'http://www.sr1wxz.ampr.org/wx.html' 
        # Send a GET request to the URL
        response = requests.get(url)

        if response.status_code == 200:
            
            soup = BeautifulSoup(response.text, 'html.parser')

            info_element = soup.find('big')

            pressure = int(info_element.text.split('\n')[4].split()[1]) # value in hPa

        return pressure

    def get_temperature(self, precision=2):
        temperature = self.bme280.temperature
        rounded_temperature = round(temperature, precision)
        return rounded_temperature
    
    def get_humidity(self, precision=2):
        humidity = self.bme280.humidity
        rounded_humidity = round(humidity, precision)
        return rounded_humidity

    # used to get the pressure from the device
    def get_pressure(self, precision=2):
        pressure = self.bme280.pressure
        rounded_pressure = round(pressure, precision)
        return rounded_pressure

    def get_formatted_datetime(self):
        # Get the current date and time
        current_datetime = datetime.now()
        # Format the date and time with precision to seconds
        formatted_datetime = current_datetime.strftime("%Y-%m-%d\n%H:%M")
        return formatted_datetime
    
    def get_altitude(self):
        return self.calculate_altitude(self.get_sea_level_pressure())
    
    

    
    
    

    


