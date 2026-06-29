import RPi.GPIO as GPIO
import time
import csv
import os

""" ULTRASONIC SENSOR (HC-SR04)
    - This script reads distance data from the HC-SR04 ultrasonic sensor and logs it to a CSV file.
"""
# --- SETUP ---
GPIO.setmode(GPIO.BCM)
TRIG_PIN = 17  # GPIO pin for Trigger
ECHO_PIN = 27  # GPIO pin for Echo
LED_PIN = 22  # GPIO pin for LED indicator
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

cwd = os.getcwd()  # Get the current working directory
Cs = 34320  # Speed of sound in cm/s
MAX_DISTANCE = 20  # Maximum distance to measure (in cm)
path = os.path.join(cwd, "distance_measurements.csv")
path_a = os.path.join(cwd, "polar.csv")
# Random error measurement constants
N = 100
R_DISTANCES = [5, 10, 15]

# --- FUNCTIONS ---
def measure_distance():
    """Measures the distance using the HC-SR04 ultrasonic sensor."""
    # STEP 1: start condition
    GPIO.output(TRIG_PIN, GPIO.LOW)
    # Pull TRIG pin high
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    # Pause for 10 us
    time.sleep(0.00001)
    # Pull TRIG pin low
    GPIO.output(TRIG_PIN, GPIO.LOW)
    
    # Wait for ECHO pin to go high
    while GPIO.input(ECHO_PIN) == 0:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on LED indicator
        time_start = time.time()

    # Wait for ECHO pin to go low
    while GPIO.input(ECHO_PIN) == 1:
        time_end = time.time()
        GPIO.output(LED_PIN, GPIO.LOW)  # Turn off LED indicator

    # Calculate elapsed time and distance
    d_time = time_end - time_start
    x_distance = (d_time * Cs) / 2  # Distance in centimeters (cm)

    # Check if distance exceeds maximum distance
    if x_distance > MAX_DISTANCE:
        x_distance = -1  # Indicate out of range

    return x_distance

def test():
    """Continuously measures distance and prints it to the console."""
    try:
        while True:
            distance = measure_distance()
            print(f"Measured distance: {distance:.3f} cm")
            time.sleep(0.5)  # Delay between measurements
    except KeyboardInterrupt:
        print("Exiting test mode.")

def measurement_1():
    """Performs a single distance measurement and compares with measurement entered by user"""
    try:    
        while True:
            x_meas = measure_distance()
            print(f"Measured distance: {x_meas:.3f} cm")
            x_real = float(input("Enter the actual distance (in centimeters): "))
            error = abs(x_meas - x_real) * 100
            print(f"Error: {error:.3f} %")
            if error > 10:
                print("Warning: Large measurement error detected!")
                break
    
    except KeyboardInterrupt:
        print("Exiting Measurement 1.")

def measurement_2():
    """Performs multiple distance measurements and logs the data to a CSV file."""
    try:
        for r in R_DISTANCES:
            print(f"Measuring distance at {r} cm...")
            with open(path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([f"Distance Measurement at {r} cm"])  # Write distance to CSV
                writer.writerow(["Measurement Number", "Distance (cm)"])  # Write header to CSV
            
            # Wait for user to confirm ready
            input(f"Place the object at {r} cm and press Enter to start measurements...")
            for i in range(N):
                x_meas = measure_distance()
                print(f"Measurement {i+1}: {x_meas:.3f} cm")
                with open(path, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([i+1, x_meas])  # Log measurement to CSV
                time.sleep(0.1)  # Delay between measurements
            print(f"Completed {N} measurements at {r} cm.")
    
    except KeyboardInterrupt:
        print("Exiting Measurement 2.")
        file.close()

def measurement_3():
    """Performs a single distance measurement and logs the data to a CSV file."""
    ANGLES = [-45, -35, -25, -15, -5, 0, 5, 15, 25, 35, 45]  # Angles in degrees
    DISTANCES = [3, 6, 9, 11]  # Distances in centimeters

    # File header (distances in each column)
    data_file = open(path_a, "w")
    data_file.write("Distances (cm):,")
    for ii in DISTANCES:
        if ii == DISTANCES[-1]:
            data_file.write(str(ii)+"\n")
        else:
            data_file.write(str(ii)+",")

    try:
        for ii in ANGLES:
            data_file.write(str(ii)+"deg,")
            for jj in DISTANCES:
                print(f"Measuring at {ii} and {jj} cm")
                while True:
                    input("\tHit enter when ready...")
                    dist = measure_distance()
                    print(f"\tMeasured distance = {dist} cm")
                    val = input("\t\tRecord? (1 = y, 0 = n)")
                    if (int(val)==1):
                        if jj == DISTANCES[-1]:
                            data_file.write(str(dist)+"\n")
                        else:
                            data_file.write(str(dist)+",")
                        break
        data_file.close()
    except KeyboardInterrupt:
        print("Exiting Measurement 3.")
        data_file.close()    
       
try:
    while True:
        print("\n--- HC-SR04 Ultrasonic Sensor Measurement Modes ---")
        print("1. Single measurement with user input")
        print("2. Multiple measurements with CSV logging")
        print("3. Polar measurements with CSV logging")
        print("Press Ctrl+C to exit at any time.")
        mode = input("Enter the mode number (1, 2, or 3): ")
        
        match mode:
            case "1":
                print("measurement_1()")
                measurement_1()
            case "2":
                print("measurement_2()")
                measurement_2() 
            case "3":
                print("measurement_3()") 
                measurement_3()
            case "test":
                print("test()")
                test()
            case _:
                print("Invalid selection. Please enter 1, 2, or 3.")
       
    
except KeyboardInterrupt:
    print("\nExiting program.")

