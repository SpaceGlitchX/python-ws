import time
import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD

""" LCD DISPLAY
    - This script initializes a 16x2 LCD display to confirm that the display is working properly.
    - Pin wiring: VSS -> GND, VDD -> 5V, V0 -> POTENTIOMETER, RS=25, RW=GND, D4=23, D5=8, D6=7, D7=14, A=5V, K=GND
    """

lcd = CharLCD(numbering_mode=GPIO.BCM, cols=16, rows=2, pin_rs=25, pin_e=24, pins_data=[23, 8, 7, 14])

try:
    lcd.clear()
    while True:
        lcd.cursor_pos = (2, 0)
        lcd.write_string(f"LCD Display Test")
        print("LCD Display Test")
        time.sleep(1)

except KeyboardInterrupt:
    lcd.clear()
    lcd.close(clear=True)
    GPIO.cleanup()  
    print("LCD Display Test stopped.")
