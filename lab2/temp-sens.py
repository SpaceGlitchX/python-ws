import time
import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD
## Temperature Sensor and LCD Display

SENSOR_ID = "22-0000001ccc5f"
DEVICE_PATH = f"/sys/bus/w1/devices/{SENSOR_ID}/w1_slave"

# Initialize LCD (using 4-bit mode and the GPIO pin mapping)
lcd = CharLCD(numbering_mode=GPIO.BCM, cols=16, rows=2, pin_rs=26, pin_e=19, pins_data=[21, 20, 16, 12])

def read_raw_temp():
    """Reads the raw temperature data from the sensor's device file."""
    with open(DEVICE_PATH, "r") as f:
        lines = f.readlines()
    return lines

def read_temp():
    """Parses the raw temperature data and returns the temperature in Celsius."""
    lines = read_raw_temp()
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = read_raw_temp()
    equals_pos = lines[1].find("t=")
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    
try:
    lcd.clear()
    while True:
        temperature = read_temp()
        lcd.cursor_pos = (0, 0)
        lcd.write_string(f"Temp: {temperature:.2f} C")  
        print(f"Current Temperature: {temperature:.2f} °C")
        time.sleep(1)
except KeyboardInterrupt:
    lcd.clear()
    print("Temperature reading stopped.")