import smbus
import time

#Fill in register info (Use Hex addresses)
MPU_I2C_ADDR = 0x68
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
ACCEL_CONFIG = 0x1C
GYRO_CONFIG  = 0x1B
# Masks
AFS_SEL_MASK = 0x18

# Constants
AFS = [2, 4, 8, 16]

def read_data(addr):
    # Left shift high data by 8 bits and concatenate with low data for 16-bit measurement
    value = ((bus.read_byte_data(MPU_I2C_ADDR, addr) << 8) | bus.read_byte_data(MPU_I2C_ADDR, addr+1))
        
    #Signed value
    if(value > 32768):
        value = value - 65536
    return value

def set_accel_FS(FS_g):
    # Determine AFS_SEL value to write
    if (FS_g == 2):
        AFS_SEL_write = 0
    elif (FS_g == 4):
        AFS_SEL_write = 1
    elif (FS_g == 8):
        AFS_SEL_write = 2
    elif (FS_g == 16):
        AFS_SEL_write = 3
    else:
        print("Please specify a full-scale accelerometer range of +/-2, 4, 8, or 16 g.")
        return -1
    
    # Change the full-scale range here 
    bus.write_byte_data(MPU_I2C_ADDR, ACCEL_CONFIG, AFS_SEL_write << 3)

    # Allow settling time for write
    time.sleep(0.25) 
    
    # Read AFS_SEL from register with masking
    AFS_SEL_read = (bus.read_byte_data(MPU_I2C_ADDR, ACCEL_CONFIG)& AFS_SEL_MASK) >> 3
    
    print("The full-scale accelerometer range is +/- "+str(AFS[AFS_SEL_read])+" g.")
    
    # Check that the written value matches the read value. Return -1 if no match.
    if (AFS_SEL_write == AFS_SEL_read):
        print("AFS_SEL_write: ", AFS_SEL_write ,"AFS_SEL_read: " ,AFS_SEL_read)
        return AFS_SEL_read
    else:
        return -1
def set_gyro_FS(FS_rot):

    if FS_rot == 250:
        value = 0
    elif FS_rot == 500:
        value = 1
    elif FS_rot == 1000:
        value = 2
    elif FS_rot == 2000:
        value = 3
    else:
        print("Invalid gyroscope range")
        return

    bus.write_byte_data(MPU_I2C_ADDR,
                         GYRO_CONFIG,
                         value << 3)


ranges = [250, 500, 1000, 2000]

for FS in ranges:

    set_gyro_FS(FS)

    data = smbus.read_byte_data(
        MPU_I2C_ADDR,
        GYRO_CONFIG
    )

    selected = (data & 0x18) >> 3

    print("Range:", FS, "deg/s")
    print("FS_SEL:", selected)

# Setup - leave this for now
bus = smbus.SMBus(1)
bus.write_byte_data(MPU_I2C_ADDR, 0x19, 7)
bus.write_byte_data(MPU_I2C_ADDR, 0x6B, 1)
bus.write_byte_data(MPU_I2C_ADDR, 0x1A, 0)
bus.write_byte_data(MPU_I2C_ADDR, 0x1B, 24)
bus.write_byte_data(MPU_I2C_ADDR, 0x38, 1)

# Part 1: Reading and writing to accelerometer full scale register
for ii in AFS:
    AFS_SEL_val = set_accel_FS(ii)

# Part 2: Set 