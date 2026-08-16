import os
import smbus
import time
import csv

""" MPU6050 SENSOR DATA LOGGING
    LAB 5 - PART 4

    Accelerometer:
    - Full-scale range: +/-16 g
    - Sample rate: 50 Hz
    - Measurement time: 10 seconds
"""

# --------------------------------------------------
# SETUP
# --------------------------------------------------

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


# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

def read_data(addr):
    """Reads data from the specified MPU6050 register."""

    # Read high byte and low byte
    value = ((bus.read_byte_data(MPU_I2C_ADDR, addr) << 8) |
             bus.read_byte_data(MPU_I2C_ADDR, addr + 1))

    # Convert to signed 16-bit value
    if value > 32768:
        value = value - 65536

    return value


def log_data(*args):
    """Logs sensor data to a CSV file."""

    with open(path, mode="a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(list(args))


# --------------------------------------------------
# START I2C BUS
# --------------------------------------------------

bus = smbus.SMBus(1)


# --------------------------------------------------
# MPU6050 SETUP
# --------------------------------------------------

# Sample rate divider
bus.write_byte_data(MPU_I2C_ADDR, 0x19, 7)

# Wake up MPU6050
bus.write_byte_data(MPU_I2C_ADDR, 0x6B, 1)

# Digital low-pass filter
bus.write_byte_data(MPU_I2C_ADDR, 0x1A, 0)

# Gyroscope full-scale range
# 24 = 0b00011000
# FS_SEL = 3
# Therefore +/-2000 deg/s
bus.write_byte_data(MPU_I2C_ADDR, GYRO_CONFIG, 24)

# Interrupt enable
bus.write_byte_data(MPU_I2C_ADDR, 0x38, 1)


# --------------------------------------------------
# PART 4
# ACCELEROMETER +/-16 g
# --------------------------------------------------

# AFS_SEL = 3
# Shift left by 3 places to bits 3 and 4
#
# 3 << 3 = 24
#
# Therefore:
# +/-16 g range

bus.write_byte_data(
    MPU_I2C_ADDR,
    ACCEL_CONFIG,
    3 << 3
)

# Allow time for setting to take effect
time.sleep(0.25)


# --------------------------------------------------
# CREATE CSV FILE
# --------------------------------------------------

cwd = os.getcwd()

path = os.path.join(
    cwd,
    "mpu6050_data_16g_50Hz.csv"
)


# --------------------------------------------------
# WRITE CSV HEADER
# --------------------------------------------------

with open(path, mode="w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Accelerometer Range: +/-16 g"
    ])

    writer.writerow([
        "Sample Rate: 50 Hz"
    ])

    writer.writerow([
        "Timestamp",
        "Ax",
        "Ay",
        "Az",
        "Gx",
        "Gy",
        "Gz",
        "Tt"
    ])


# --------------------------------------------------
# DATA COLLECTION
# --------------------------------------------------

try:

    print("Starting measurement...")
    print("Accelerometer range: +/-16 g")
    print("Sample rate: 50 Hz")
    print("Measurement time: 10 seconds")

    start_time = time.time()

    # 50 samples/second x 10 seconds
    N = Fs * 10

    for x in range(N):

        # ------------------------------------------
        # READ ACCELEROMETER
        # ------------------------------------------

        acc_x = read_data(ACCEL_XOUT_H)
        acc_y = read_data(ACCEL_YOUT_H)
        acc_z = read_data(ACCEL_ZOUT_H)


        # ------------------------------------------
        # READ GYROSCOPE
        # ------------------------------------------

        gyro_x = read_data(GYRO_XOUT_H)
        gyro_y = read_data(GYRO_YOUT_H)
        gyro_z = read_data(GYRO_ZOUT_H)


        # ------------------------------------------
        # READ TEMPERATURE
        # ------------------------------------------

        temp_t = read_data(TEMP_OUT_H)


        # ------------------------------------------
        # CONVERT ACCELEROMETER DATA
        # ------------------------------------------

        # +/-16 g sensitivity:
        # 2048 LSB/g

        Ax = acc_x / 2048.0
        Ay = acc_y / 2048.0
        Az = acc_z / 2048.0


        # ------------------------------------------
        # CONVERT GYROSCOPE DATA
        # ------------------------------------------

        # +/-2000 deg/s sensitivity:
        # 16.4 LSB/(deg/s)

        Gx = gyro_x / 16.4
        Gy = gyro_y / 16.4
        Gz = gyro_z / 16.4


        # ------------------------------------------
        # CONVERT TEMPERATURE
        # ------------------------------------------

        Tt = (temp_t / 340.00) + 36.53


        # ------------------------------------------
        # TIMESTAMP
        # ------------------------------------------

        elapsed_time = time.time() - start_time


        # ------------------------------------------
        # SAVE DATA
        # ------------------------------------------

        log_data(
            elapsed_time,
            Ax,
            Ay,
            Az,
            Gx,
            Gy,
            Gz,
            Tt
        )


        # ------------------------------------------
        # WAIT FOR NEXT SAMPLE
        # ------------------------------------------

        time.sleep(1 / Fs)


    print("Data logging completed.")
    print("File saved as:")
    print(path)


except KeyboardInterrupt:

    print("Data logging stopped.")