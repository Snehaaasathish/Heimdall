import RPi.GPIO as GPIO # Required to access gpio pins on the raspberry pi
from time import sleep

GPIO.setmode(GPIO.BOARD)
pinno = 3 # Pin to which servo is connected

GPIO.setup(pinno, GPIO.OUT)
pwm=GPIO.PWM(pinno, 50)
pwm.start(0)

def SetAngle(angle): # Sets the angle of the servo according to the parameter.
	duty = angle / 18 + 2
	GPIO.output(pinno, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(pinno, False)
	pwm.ChangeDutyCycle(0)

pwm.stop()
GPIO.cleanup()    
 
