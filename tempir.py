from mlx90614 import MLX90614
import servo as sp
import time
import RPi.GPIO as GPIO
thermometer_address = 0x5a
thermometer = MLX90614(thermometer_address)
sensor = 16
tpr = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor,GPIO.IN)
GPIO.setup(tpr,GPIO.OUT)

GPIO.output(tpr,False)

try: 
   while True:
      if GPIO.input(sensor):
          temp=thermometer.get_obj_temp()
          if 36.1<=temp<=37.2
              sp.setAngle()
              sleep(30)
      else
          temp=-1
      GPIO.output(tpr,False)    
except KeyboardInterrupt:
    GPIO.cleanup()
 
