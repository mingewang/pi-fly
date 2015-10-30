import math
import time
import imp
from sys import version_info

try:
    imp.find_module('RPIO')
    import RPIO as GPIO
    rpio = True
except ImportError:
    import RPi.GPIO as GPIO
    print("Warning, module RPIO not found falling back to GPIO.")
    print("PWM is now disabled.")
    rpio = False

if version_info[0] <= 2:
    print("Error: Python version is not compatible with this code.")
    exit()

updown_pin = 11
neutral_pin = 13
right_pin = 15
stationary_pin = 16
backward_pin = 18

pin_list = [updown_pin, neutral_pin, right_pin, stationary_pin, backward_pin]
checkpoints = {}
flight_data = {
    "checkpoints": checkpoints,
    "pin_list": pin_list
}

GPIO.setmode(GPIO.BOARD)  # Set pin numbering to board layout
GPIO.setup(pin_list, GPIO.OUT, intial=GPIO.LOW)  # Set pins as output, GPIO.LOW is same as 0 and False
GPIO.output(neutral_pin, 1)
GPIO.output(stationary_pin, 1)

if (rpio is True or rpio == 1):
    servo = GPIO.PWM.Servo()  # PWM module uses servo everywhere, so we do to

    def pwm(pin, state):
        if state == 0:
            servo.stop_servo(pin)
        elif state > 0 and state <= 1:
            tmp_var = state * 20000
            servo.set_servo(pin, tmp_var)
        else:
            print("Error: value not recognised, please make sure it is between 0 and 1.")
else:
    def pwm(pin, state):
        if state >= 0.5:
            GPIO.output(pin, 1)
        elif state < 0.5:
            GPIO.output(pin, 0)
        else:
            print("Error: value not recognised, please make sure it is between 0 and 1.")


def n_c(n):  # Checks if input is numeric
    if type(n) == int or type(n) == float:
        return True
    else:
        return False


def flight_path(user_input):
    if user_input == "print":
        if bool(checkpoints) == True:
            print("This is the flight path:")
            for i, j in sorted(checkpoints.items()):
                print(i, ":", j)
        else:
            print("Sorry no flight path is set.")
    elif user_input == "delete":
        u_input = input("Are you sure you want to delete the flight path?").lower()
        if u_input == "yes" or u_input == "y":
            checkpoints = {}
            print("The flight path has been deleted.")
        else:
            print("The flight path has not been deleted.")
    else:
        print("Error: unknown command.")


def set_checkpointpoint(x, y, z, w):
    if n_c(x) == True and n_c(y) == True and n_c(z) == True and n_c(w) == True:
        checkpoint = "Checkpoint " + str(w)
        checkpoints[checkpoint] = [x, y, z]
    else:
        print("Error: values not numeric")
'''
for k, v in sorted(d.items()):
    print k, ':', v

    or

for k in sorted(d):
   print d[k]






















'''


def updown(thrust, air_time):  # Thrust is a value between 0 and 1
    if 0 <= thrust <= 1:
        pwm(updown_pin, 1)
        time.sleep(air_time)
        pwm(updown_pin, 0)
    else:
        print("Error")
    return


def leftright(direction, air_time):
    if direction == "left":
        GPIO.output(updown_pin, 1)
        GPIO.output(neutral_pin, 0)
        time.sleep(air_time)
        GPIO.output(neutral_pin, 1)
        GPIO.output(updown_pin, 0)
    elif direction == "right":
        GPIO.output(updown_pin, 1)
        GPIO.output(neutral_pin, 0)
        GPIO.output(right_pin, 1)
        time.sleep(air_time)
        GPIO.output(right_pin, 0)
        GPIO.output(neutral_pin, 1)
        GPIO.output(updown_pin, 0)
    else:
        print("Error")
    return


def forwardbackward(direction, air_time):
    if direction == "forward":
        GPIO.output(updown_pin, 1)
        GPIO.output(stationary_pin, 0)
        time.sleep(air_time)
        GPIO.output(stationary_pin, 1)
        GPIO.output(updown_pin, 0)
    elif direction == "backward":
        GPIO.output(updown_pin, 1)
        GPIO.output(stationary_pin, 0)
        GPIO.output(backward_pin, 1)
        time.sleep(air_time)
        GPIO.output(backward_pin, 0)
        GPIO.output(stationary_pin, 1)
        GPIO.output(updown_pin, 0)
    else:
        print("Error")
    return

error = 0

while True:
    user_input = input("You have the following options: up, left/right, forward/backward and exit, default air_time at the moment is 5 seconds.").lower()
    if user_input == "exit":
        break
    elif user_input == "up":
        updown(1, 5)
        error = 0
    elif user_input == "left" or user_input == "right":
        leftright(user_input, 5)
        error = 0
    elif user_input == "forward" or user_input == "backward":
        forwardbackward(user_input, 5)
        error = 0
    else:
        print("An error occured, please try again and check your spelling.")
        error = error + 1
        if error >= 3:
            print("Too many errors occured, exiting now.")
            break

GPIO.cleanup()
exit()
