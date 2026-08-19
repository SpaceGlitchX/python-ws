import RPi.GPIO as GPIO
import time

# Constants
CLK = 17
SW = 27
DT = 18

# Global position
Pos = 0

# Encoder resolution
DEGREES_PER_STEP = 360 / 20

# Setup GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Event-driven call-back
def signal_event(channel):
    global Pos
    # Read pin states
    clk_state = GPIO.input(CLK)
    dt_state = GPIO.input(DT)
    sw_state = GPIO.input(SW)
    
    # CLK triggered = encoder rotated
    if channel == CLK:
        print("CLK line triggered.")
        
        # Determine direction
        if dt_state == GPIO.LOW:
            # Counter-clockwise
            Pos += DEGREES_PER_STEP
            
        else:
            # Clockwise
            Pos = Pos-DEGREES_PER_STEP
    elif channel == SW:
        
        print("SW line trigger.")
        Pos = 0
        # Reset position
        
    # Print logic states
    print("CLK = ", clk_state)
    print("DT = ", dt_state)
    print("SW = ", sw_state)
    
    # Print position
    print("Position = ", Pos, "degrees")
    
# Define interrupt-driven events
GPIO.add_event_detect(CLK, GPIO.FALLING, callback = signal_event, bouncetime = 200)
GPIO.add_event_detect(SW, GPIO.FALLING, callback = signal_event, bouncetime = 200)


# Main loop
try:
    print("Encoder running...")
    print("Turn encoder to change position.")
    print("Press button to reset position.")
    print("Press Ctrl+C to stop.")

    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nProgram stopped.")

finally:
    GPIO.cleanup()