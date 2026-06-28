import time
import csv
import os
import matplotlib.pyplot as plt

""" TEMPERATURE SENSOR AND LCD DISPLAY
    - This script reads temperature data from a DS18B20 sensor and displays it on a 16x2 LCD.
    -"""

# --- SETUP ---
# Temperature sensor configuration
SENSOR_ID = "22-0000001ccc5f"
DEVICE_PATH = f"/sys/bus/w1/devices/{SENSOR_ID}/w1_slave"

x_time = []
y_temp = []

N = 200 # Iterations
cwd = os.getcwd()  # Get the current working directory
path = os.path.join(cwd, "temperature_samples(12bit).csv")  # Path to the CSV log file

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
    
def log_temperature(temp):
    """Logs the temperature to a CSV file."""
    with open(path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime("%H:%M:%S"), temp])
try:
    with open(path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Temperature (C)"])  # Write header to CSV
    start_time = time.time()  # Record the start time

    for _ in range(N):
        temperature = read_temp()
        print(f"Current Temperature: {temperature:.2f} °C")
        log_temperature(temperature)
        x_time.append(time.time() - start_time)
        y_temp.append(temperature)
        time.sleep(1)
    
    # Plot the temperature data
    plt.plot(x_time, y_temp)
    plt.xlabel("Time (s)")
    plt.ylabel("Temperature (C)")
    plt.title("Temperature vs Time")
    plt.savefig(os.path.join(cwd, "temperature_plot(12bit).png"))  # Save the plot as an image
    plt.show()
    
    print("Temperature reading stopped.")
except KeyboardInterrupt:
    print("Temperature reading stopped.")