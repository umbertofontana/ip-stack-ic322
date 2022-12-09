import RPi.GPIO as GPIO
import time

def fire():
    # set the board numbering scheme
    GPIO.setmode(GPIO.BOARD)

    # set the pin to output
    GPIO.setup(12, GPIO.OUT)

    for i in range(5):
        print("high")
        GPIO.output(12, GPIO.HIGH)
        time.sleep(1)
        print("low")
        GPIO.output(12, GPIO.LOW)
        time.sleep(1)


    GPIO.cleanup()


