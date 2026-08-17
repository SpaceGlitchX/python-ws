import os
import smbus
import time
import csv
import matplotlib.pyplot as plt

""" MPU6050 SENSOR DATA LOGGING
    LAB 5 - PART 5

    Gyroscope comparison:
    - +/-250 deg/s
    - +/-2000 deg/s
    - 50 Hz
    - 10 seconds
"""
# SETUP

MPU_I2C_ADDR = 0x68

ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F

GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

TEMP_OUT_H = 0x41

ACCEL_CONFIG = 0x1C
GYRO_CONFIG = 0x1B

# Sample rate
Fs = 50

# Measurement time
duration = 10

def read_data(addr):
    """Reads 16-bit signed data from the MPU6050."""

    value = ((bus.read_byte_data(MPU_I2C_ADDR, addr) << 8) |
            bus.read_byte_data(MPU_I2C_ADDR, addr + 1))

    # Convert to signed value
    if value > 32768:
        value = value - 65536

    return value

def log_data(path, *args):
    """Logs sensor data to a CSV file."""

    with open(path, mode="a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(list(args))

# START I2C BUS
bus = smbus.SMBus(1)

# MPU6050 SETUP
# Sample rate divider
bus.write_byte_data(MPU_I2C_ADDR, 0x19, 7)

# Wake up MPU6050
bus.write_byte_data(MPU_I2C_ADDR, 0x6B, 1)

# Digital low-pass filter
bus.write_byte_data(MPU_I2C_ADDR, 0x1A, 0)

# Accelerometer left at +/-2 g
bus.write_byte_data(MPU_I2C_ADDR, ACCEL_CONFIG, 0)

# Enable interrupt
bus.write_byte_data(MPU_I2C_ADDR, 0x38, 1)

# GYROSCOPE RANGE
gyro_ranges = [250, 2000]

# MEASURE BOTH GYROSCOPE RANGE
try:

    for gyro_range in gyro_ranges:

        # SET GYROSCOPE RANGE
        
        if gyro_range == 250:

            # FS_SEL = 0
            gyro_setting = 0
            sensitivity = 131.0

        elif gyro_range == 2000:

            # FS_SEL = 3
            gyro_setting = 3
            sensitivity = 16.4

        # Write FS_SEL to bits 3 and 4
        bus.write_byte_data(
            MPU_I2C_ADDR,
            GYRO_CONFIG,
            gyro_setting << 3
        )

        time.sleep(0.25)

        # CREATE CSV FILE

        cwd = os.getcwd()

        path = os.path.join(
            cwd,
            f"mpu6050_gyro_{gyro_range}dps_50Hz.csv"
        )

        # WRITE HEADER

        with open(path, mode="w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                f"Gyroscope Range: +/-{gyro_range} deg/s"
            ])

            writer.writerow([
                f"Sample Rate: {Fs} Hz"
            ])

            writer.writerow([
                "Timestamp",
                "Gx",
                "Gy",
                "Gz"
            ])

        # DATA COLLECTION
        print()
        print(
            f"Logging gyroscope at +/-{gyro_range} deg/s "
            f"for {duration} seconds..."
        )

        start_time = time.time()

        N = Fs * duration

        gx_values = []
        time_values = []

        for x in range(N):

            # Read gyroscope
            gyro_x = read_data(GYRO_XOUT_H)
            gyro_y = read_data(GYRO_YOUT_H)
            gyro_z = read_data(GYRO_ZOUT_H)

            Gx = gyro_x / sensitivity
            Gy = gyro_y / sensitivity
            Gz = gyro_z / sensitivity

            # Timestamp
            elapsed_time = time.time() - start_time

            # Save data
            log_data(
                path,
                elapsed_time,
                Gx,
                Gy,
                Gz
            )

            # Maintain 50 Hz
            time.sleep(1 / Fs)
        print(
            f"Completed +/-{gyro_range} deg/s measurement."
        )

except KeyboardInterrupt:

    print("Data logging stopped.")