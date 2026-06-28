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

try:
    while True:
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

        print(f"Measured Distance: {x_distance:.2f} cm")
except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO settings on exit