import RPi.GPIO as GPIO
from time import sleep

def d2b(value):
    return [int(element) for element in bin(value)[2:].zfill(8)] 

GPIO.setwarnings(False)

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

inc_flag = 1
t = 0 
x = 0

try:
    period = float(input("Input period:"))

    while True:
        GPIO.output(dac, d2b(x))
        voltage = (x / 256) * 3.3
        print(f"Output voltage is about {voltage:.4} volt")
 
        if   x == 0:    inc_flag = 1
        elif x == 255:  inc_flag = 0

        x = x + 1 if inc_flag == 1 else x - 1

        sleep(period/512)
        t += 1

except ValueError:
    print("Wrong period")

finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup()
    