import cv2
from st7920 import ST7920
from detect_mask_image import mask
from mlx90614 import MLX90614
from Bluetin_Echo import Echo
import RPi.GPIO as GPIO
from servo import SetAngle
from time import sleep
# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# To capture video from webcam. Try 0 instead of 1 in the arguement if
# you only have one webcam.
cap = cv2.VideoCapture(1)
#frame count keeps track of the number of frames a face is centered in the
# video
fc = 0
# tolerance count is the minimum number of frames a face can be absent from
# center
tc = 5
# Create display object
s = ST7920()
# Initialize mlx90614 address
thermometer_address = 0x5a
# Create temperature sensor instance
temp = MLX90614(thermometer_address)
#defining values for ultrasonic sensor
TRIGGER_PIN = 8
ECHO_PIN = 7
speed_of_sound = 340
echo = Echo(TRIGGER_PIN, ECHO_PIN, speed_of_sound)
# Initializing servo motor
GPIO.setmode(GPIO.BOARD)
servo = 4 # Pin to which servo is connected
GPIO.setup(servo, GPIO.OUT)
pwm=GPIO.PWM(servo, 50)
pwm.start(0)
# Initializing dc pump
GPIO.setmode(GPIO.BOARD)
pump_pin = 21
GPIO.setup(pump_pin, GPIO.OUT)
GPIO.output(pump_pin,False)
# Initializing ir sensor
GPIO.setmode(GPIO.BOARD)
ir_sensor = 26
GPIO.setup(ir_sensor, GPIO.IN)

s.clear()
s.put_text("Please stand in the white box and await scanning",5,10)
s.redraw()

while True:
    # Read the frame
    ret, img = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # x,y is coordinate of top left corner of rectangle and w,h are
    # width and height
    x, y, w, h = 0, 0, 0, 0
    if (len(faces) != 0):
        x = faces[0][0]
        y = faces[0][1]
        w = faces[0][2]
        h = faces[0][3]
    # Calculate coordinates of face
    centerX = x + w / 2
    centerY = y + h / 2
    # Obtain dimensions of frame
    dim = img.shape
    image_height = dim[0]
    image_width = dim[1]
    # If a frame is centered for more than 50 frames then we can be sure
    # the person wants access
    if ((x > 230 and x < 270) and (y > 140 and y < 180) and fc < 50):
        s.clear()
        s.put_text("Scanning: Please do no move",5,10)
        s.redraw()
        fc = fc + 1
        tc = 5
    elif fc == 50:
        #check for other values and reinitilize in the end
        s.clear()
        s.put_text("Scan Complete: Await Processing",5,10)
        s.redraw()
        mask_flag = mask(img)
        if(not mask_flag):
            s.clear()
            s.put_text("Cannot allow without mask, please step aside from queue",5,10)
            s.redraw()
            fc = 0
            tc = 5
            break
        s.clear()
        s.put_text("Please bring forehead close to red sensor",5,10)
        s.redraw()
        distance = echo.read('cm')
        while(distance > 10):
            s.clear()
            s.put_text("Please bring forehead close to red sensor",5,10)
            s.redraw()
            distance = echo.read('cm')
        T = temp.get_obj_temp()
        if(T > 99):
            s.clear()
            s.put_text("Cannot allow due to high body temperature, please step aside from queue",5,10)
            s.redraw()
            fc = 0
            tc = 5
            break
        s.clear()
        s.put_text("Retract forehead and please bring hand close to pipe for hand sanitizer",5,10)
        s.redraw()
        if GPIO.input(ir_sensor):
            GPIO.output(pump_pin, True)
            sleep(5)
        GPIO.output(pump_pin, False)
        SetAngle(110)
        sleep(20)
        SetAngle(0)
        fc = 0
        tc = 5
    elif tc <= 0 :
        fc = 0
        tc = 5
    else :
        tc = tc-1

    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# Release the VideoCapture object
cap.release()
cv2.destroyAllWindows()
