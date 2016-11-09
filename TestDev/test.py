import Adafruit_BBIO.GPIO as GPIO
Left_line = "P9_23"
Right_line = "P9_28"
GPIO.setup(Left_line, GPIO.IN)
GPIO.setup(Right_line, GPIO.IN)
while True:
    print(GPIO.input(Left_line))
    print(GPIO.input(Right_line))
