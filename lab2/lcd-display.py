import time
import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD

""" LCD DISPLAY
    - This script initializes a 16x2 LCD display to confirm that the display is working properly.
    - Pin wiring: VSS -> GND, VDD -> 5V, V0 -> POTENTIOMETER, RS=26, RW=GND, D4=21, D5=20, D6=16, D7=12, A=5V, K=GND
    """

lcd = CharLCD(numbering_mode=GPIO.BCM, cols=16, rows=2, pin_rs=26, pin_e=19, pins_data=[21, 20, 16, 12])

try:
    lcd.clear()
    while True:
        lcd.cursor_pos = (0, 0)
        lcd.write_string(f"LCD Display Test")
        print("LCD Display Test")
        time.sleep(1)

except KeyboardInterrupt:
    lcd.clear()
    lcd.close(clear=True)
    GPIO.cleanup()  
    print("LCD Display Test stopped.")
