import RPi.GPIO as gpio

def d2b(value):
    return [int(element) for element in bin(value)[2:].zfill(8)] 

def is_float(string):
    if string.replace(".", "").isnumeric():
        return True
    else:
        return False

dac = [8, 11, 7, 1, 0, 5, 12, 6]

gpio.setmode(gpio.BCM)
gpio.setup(dac, gpio.OUT)

try:
    while True:
        print("Enter number:")
        str = input()
        try:
            if (not str.lstrip('+-').isnumeric()):
                print("Input number")
            elif (not is_float(str.lstrip('+-'))):
                print("Input whole number")
            elif (int(str) < 0):
                print("Input positive number")
            elif (int(str) > 255):
                print("Input number between 0 and 255")
            else:    
                num = int(str)
                conv = d2b(num)
                gpio.output(dac, conv)
                voltage = float(num) / 256.0 * 3.3
                print(f"Output voltage is about {voltage:.4} volt")
        except Exception:
            if (num == 'q'): 
                print("quit")
                break
finally:
    gpio.output(dac, gpio.LOW)
    gpio.cleanup()