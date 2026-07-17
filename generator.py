import time
import lgpio

GPIO_PIN = 22
FREQ = 100  # Frequency in Hz

h = lgpio.gpiochip_open(0)  # Open the GPIO chip
lgpio.gpio_claim_output(h, GPIO_PIN)  # Claim the GPIO pin for output

print(f"Generating a {FREQ} Hz square wave on GPIO pin {GPIO_PIN}...")
print("Press Ctrl+C to stop.")

try:
    lgpio.tx_square_wave(h, GPIO_PIN, FREQ)  # Start generating the square wave
    while True:
        time.sleep(1)  # Keep the program running

except KeyboardInterrupt:
    print("\nStopping signal...")

finally:
    lgpio.tx_cancel(h, GPIO_PIN)  # Stop generating the square wave
    lgpio.gpio_free(h, GPIO_PIN)  # Close the GPIO chip
    lgpio.gpiochip_close(h)  # Close the GPIO chip
    print("Signal generation stopped.")