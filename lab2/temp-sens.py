import time
import csv
import os
import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD

""" TEMPERATURE SENSOR AND LCD DISPLAY
    - This script reads temperature data from a DS18B20 sensor and displays it on a 16x2 LCD.
    -"""

# --- SETUP ---
# Temperature sensor configuration
SENSOR_ID = "22-0000001ccc5f"
DEVICE_PATH = f"/sys/bus/w1/devices/{SENSOR_ID}/w1_slave"

# Initialize LCD
lcd = CharLCD(numbering_mode=GPIO.BCM, cols=16, rows=2, pin_rs=26, pin_e=19, pins_data=[21, 20, 16, 12])

N = 20 # Iterations
threshold = 23.00 # Threshold temperature in Celsius
th_pin = 18 # Pin for threshold indicator
GPIO.setup(th_pin, GPIO.OUT)  # Set up the threshold indicator pin as output
cwd = os.getcwd()  # Get the current working directory
path = os.path.join(cwd, "temperature_log.csv")  # Path to the CSV log file

# --- FUNCTIONS ---
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
    
def check_threshold(temp):
    """Checks if the temperature exceeds the threshold and blinks the indicator led if it does."""
    if temp > threshold:
        blink_count = 5  # Number of times to blink the LED
        for _ in range(blink_count):
            GPIO.output(th_pin, GPIO.HIGH)  # Turn on indicator
            time.sleep(0.05)
            GPIO.output(th_pin, GPIO.LOW)  # Turn off indicator
            time.sleep(0.05)
    else:
        GPIO.output(th_pin, GPIO.LOW)  # Turn off indicator

def log_temperature(temp):
    """Logs the temperature to a CSV file."""
    with open(path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), temp])
try:
    lcd.clear()
    with open(path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Temperature (C)"])  # Write header to CSV

    for _ in range(N):
        temperature = read_temp()
        lcd.cursor_pos = (0, 0)
        lcd.write_string(f"Temp: {temperature:.2f} C")  
        print(f"Current Temperature: {temperature:.2f} °C")
        check_threshold(temperature)
        log_temperature(temperature)
        time.sleep(1)
    
    lcd.clear()
    print("Temperature reading stopped.")
except KeyboardInterrupt:
    lcd.clear()
    print("Temperature reading stopped.")