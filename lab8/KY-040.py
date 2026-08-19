import RPi.GPIO as GPIO
import time

# Constants
CLK = 17
SW = 27
DT = 18

RED = 22
GREEN = 23
BLUE = 24

# [R, G, B]
RGB_intensity = [255, 0, 0]

# 0 = R, 1 = G, 2 = B
colour_select = 0

# Encoder resolution
DEGREES_PER_STEP = 360 / 20

# Setup GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)

# Setup PWMs
red_pwm = GPIO.PWM(RED, 1000)
green_pwm = GPIO.PWM(GREEN, 1000)
blue_pwm = GPIO.PWM(BLUE, 1000)

red_pwm.start(0)
green_pwm.start(0)
blue_pwm.start(0)

# Update RGB
def update_colour():

    # Convert 0-255 to 0-100%
    red_duty = (RGB_intensity[0] / 255) * 100
    green_duty = (RGB_intensity[1] / 255) * 100
    blue_duty = (RGB_intensity[2] / 255) * 100

    red_pwm.ChangeDutyCycle(red_duty)
    green_pwm.ChangeDutyCycle(green_duty)
    blue_pwm.ChangeDutyCycle(blue_duty)
    
def signal_event(channel):

    global RGB_intensity
    global colour_select

    # Read encoder states
    clk_state = GPIO.input(CLK)
    dt_state = GPIO.input(DT)
    sw_state = GPIO.input(SW)
    
    if channel == CLK:

        # 10% of 255 = 25.5
        change = 26

        # Counter-clockwise
        if dt_state == GPIO.LOW:

            RGB_intensity[colour_select] += change

        # Clockwise
        else:

            RGB_intensity[colour_select] -= change

        # Keep between 0 and 255
        if RGB_intensity[colour_select] > 255:
            RGB_intensity[colour_select] = 255

        if RGB_intensity[colour_select] < 0:
            RGB_intensity[colour_select] = 0

        # Convert to integer
        RGB_intensity[colour_select] = int(RGB_intensity[colour_select])

    # Encoder button
    elif channel == SW:

        # Select next colour
        colour_select += 1

        # Loop back to red
        if colour_select > 2:
            colour_select = 0

    # Update LED
    update_colour()

    # Print information
    colours = ["Red", "Green", "Blue"]

    print("-------------------------")
    print("Triggered:", "CLK" if channel == CLK else "SW")
    print("CLK:", clk_state)
    print("DT :", dt_state)
    print("SW :", sw_state)

    print("Selected colour:", colours[colour_select])
    print("RGB intensity:", RGB_intensity)
    print()

# Event detection
GPIO.add_event_detect(CLK,GPIO.FALLING,callback=signal_event,bouncetime=200)
GPIO.add_event_detect(SW,GPIO.FALLING,callback=signal_event,bouncetime=200)

# Initial LED state
update_colour()



# Main loop
try:

    print("RGB encoder program running.")
    print("Turn encoder to change intensity.")
    print("Press encoder button to select colour.")
    print("Press Ctrl+C to stop.")

    while True:
        time.sleep(0.1)

except KeyboardInterrupt:

    print("\nProgram stopped.")

finally:
    red_pwm.stop()
    green_pwm.stop()
    blue_pwm.stop()

    GPIO.cleanup()