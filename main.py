import time
import imp

try:
    imp.find_module('RPIO')
    import RPIO as GPIO
except ImportError:
    import RPi.GPIO as GPIO
    print "Warning, module RPIO not found falling back to GPIO."
    print "PWM is now disabled."

updown_pin = 11
neutral_pin = 13
right_pin = 15
stationary_pin = 16
backward_pin = 18

pin_list = [updown_pin]

GPIO.setmode(GPIO.BOARD)  # Set pin numbering to board layout
GPIO.setup(pin_list, GPIO.OUT, intial=GPIO.LOW)  # Set pins as output, GPIO.LOW is same as 0 and False
servo = GPIO.PWM.Servo()  # PWM module uses servo everywhere, so we do to

GPIO.output(neutral_pin, 1)
GPIO.output(stationary_pin, 1)

def updown(thrust, air_time):  # Thrust is a value between 0 and 1
    if 0 <= thrust <= 1:
        GPIO.output(updown_pin, 1)
        time.sleep(air_time)
        GPIO.output(updown_pin, 0)
    else:
        print "Error"
    return

def leftright(direction, air_time):
    if direction == left:
        GPIO.output(updown_pin, 1)
        GPIO.output(neutral_pin, 0)
        time.sleep(air_time)
        GPIO.output(neutral_pin, 1)
        GPIO.output(updown_pin, 0)
    elif direction == right:
        GPIO.output(updown_pin, 1)
        GPIO.output(neutral_pin, 0)
        GPIO.output(right_pin, 1)
        time.sleep(air_time)
        GPIO.output(right_pin, 0)
        GPIO.output(neutral_pin, 1)
        GPIO.output(updown_pin, 0)
    else:
        print "Error"
    return

def forwardbackward(direction, air_time):
    if direction == forward:
        GPIO.output(updown_pin, 1)
        GPIO.output(stationary_pin, 0)
        time.sleep(air_time)
        GPIO.output(stationary_pin, 1)
        GPIO.output(updown_pin, 0)
    elif direction == backward:
        GPIO.output(updown_pin, 1)
        GPIO.output(stationary_pin, 0)
        GPIO.output(backward_pin, 1)
        time.sleep(air_time)
        GPIO.output(backward_pin, 0)
        GPIO.output(stationary_pin, 1)
        GPIO.output(updown_pin, 0)
    else:
        print "Error"
    return

while exit == False:
    user_input = raw_input("You have the following options: up, left/right, forward/backward and exit, default air_time at the moment is 5 seconds.").lower()
    if user_input == exit:
        exit = True
    elif user_input == up:
        updown(1, 5)
        error = 0
    elif user_input == left or right:
        leftright(user_input, 5)
        error = 0
    elif user_input == forward or backward:
        forwardbackward(user_input, 5)
        error = 0
    else:
        print "An error occured, please try again and check your spelling."
        error = error + 1
        if error > 3:
            print "Too many errors occured, exiting now."
            exit = True

GPIO.cleanup()
exit()
