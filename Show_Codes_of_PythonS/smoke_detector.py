import RPi.GPIO as GPIO
import time
import Adafruit_ADS1x15

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define sensor pin
SENSOR_PIN = 17

# Create an ADS1115 ADC (16-bit) instance
adc = Adafruit_ADS1x15.ADS1115()

# Define threshold value
THRESHOLD = 1000  # adjust this value based on your sensor reading

try:
    while True:
        # Read sensor value
        value = adc.read_adc(0, gain=1)
        
        # Check if smoke is detected
        if value > THRESHOLD:
            print("Smoke detected!")
            # Trigger alert or notification
            # GPIO.output(LED_PIN, GPIO.HIGH)
            # GPIO.output(BUZZER_PIN, GPIO.HIGH)
        else:
            print("No smoke detected")
            # Turn off alert or notification
            # GPIO.output(LED_PIN, GPIO.LIGH)
            # GPIO.output(BUZZER_PIN, GPIO.LIGH)
        
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()