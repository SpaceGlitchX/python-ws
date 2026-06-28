import os
import smbus
import time
import csv

""" MPU6050 SENSOR DATA LOGGING
    - This script reads accelerometer and gyroscope data from the MPU6050 sensor and logs it to a CSV file.
    - Reads for sample rates of 1Hz, 5Hz, 10Hz and 50Hz for 10s"""

#Fill in register info (Use Hex addresses)
MPU_I2C_ADDR = 0x68
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
TEMP_OUT_H = 0x41

# Set sample rate
Fs = 1, 5, 10, 50  # Sample rates in Hz
N = Fs*10  # Number of iterations for data logging (10 seconds of data collection)

# Function to read data from specified memory registers.
def read_data(addr):
    """Reads data from the specified memory register address of the MPU6050 sensor."""
    # Left shift high data by 8 bits and concatenate with low data for 16-bit measurement
    value = ((bus.read_byte_data(MPU_I2C_ADDR, addr) << 8) | bus.read_byte_data(MPU_I2C_ADDR, addr+1))
        
    #Signed value
    if(value > 32768):
        value = value - 65536
    return value

def log_data(*args):
    """Logs the accelerometer and gyroscope data to a CSV file."""
    with open(path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(list(args))

# Setup - leave this alone for now
bus = smbus.SMBus(1)
bus.write_byte_data(MPU_I2C_ADDR, 0x19, 7)
bus.write_byte_data(MPU_I2C_ADDR, 0x6B, 1)
bus.write_byte_data(MPU_I2C_ADDR, 0x1A, 0)
bus.write_byte_data(MPU_I2C_ADDR, 0x1B, 24)
bus.write_byte_data(MPU_I2C_ADDR, 0x38, 1)

try:

    for Fs in [1, 5, 10, 50]:  # Iterate through the sample rates
        cwd = os.getcwd()  # Get the current working directory
        path = os.path.join(cwd, f"mpu6050_data_{Fs}Hz.csv")  # Path to the CSV log file
        
        with open(path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Ax", "Ay", "Az", "Gx", "Gy", "Gz", "Tt"])  # Write header to CSV
        start_time = time.time()  # Record the start time

        # Iterate for a given range - define the variable NUM_IT
        for x in range(N):
            acc_x = read_data(ACCEL_XOUT_H)
            acc_y = read_data(ACCEL_YOUT_H)
            acc_z = read_data(ACCEL_ZOUT_H)
            gyro_x = read_data(GYRO_XOUT_H)
            gyro_y = read_data(GYRO_YOUT_H)
            gyro_z = read_data(GYRO_ZOUT_H)
            temp_t = read_data(TEMP_OUT_H)
            #Scale the data
            Ax = acc_x / 16384.0
            Ay = acc_y / 16384.0
            Az = acc_z / 16384.0
            Gx = gyro_x / 131.0
            Gy = gyro_y / 131.0
            Gz = gyro_z / 131.0
            Tt = (temp_t/340.00)+36.53  # Convert temperature in °/c
            elapsed_time = time.time() - start_time
            # Write data to csv file
            log_data(elapsed_time, Ax, Ay, Az, Gx, Gy, Gz, Tt)
            
            # Sleep for sample period
            time.sleep(1/Fs)

except KeyboardInterrupt:
    print("Data logging stopped.")