import RPi.GPIO as GPIO
import time

# Constants
CLK = 17
SW = 23
DT = 27
DURATION = 10

# Setup GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Event-driven call-back
def signal_event(channel):
    
    if GPIO.input(CLK):
        print("CLK line triggered.")
    elif GPIO.input(SW):
        print("SW line triggered.")
        
    # Output logic states of SW, CLK, DT
    print(f"SW = {GPIO.input(SW)}\nCLK = {GPIO.input(CLK)}\nDT = {GPIO.input(DT)}\n")

# Define interrupt-driven events
GPIO.add_event_detect(CLK, GPIO.FALLING, callback = signal_event, bouncetime = 300)
GPIO.add_event_detect(SW, GPIO.FALLING, callback = signal_event, bouncetime = 300)

start = time.time()
d = time.time() - start
while d <= DURATION:
    d = time.time() - start