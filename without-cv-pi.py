import math
import time
import imp
from sys import version_info

print("Warning!")
print("The computer has no idea where to helicopter(s) are.")
print("Please use main.py if the helicopter(s) are not chained to the floor.")
print("This program is a dry-run to test the code.")
print("Please execute without-cv.py for the real program.")

try:
    imp.find_module('RPIO')
    import RPIO as GPIO
    rpio = True
except ImportError:
    '''
    import RPi.GPIO as GPIO
    '''
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

print("GPIO.setmode(GPIO.BOARD)  # Set pin numbering to board layout")
print("GPIO.setup(pin_list, GPIO.OUT, intial=GPIO.LOW)  # Set pins as output, GPIO.LOW is same as 0 and False")
print("GPIO.output(neutral_pin, 1)")
print("GPIO.output(stationary_pin, 1)")

if (rpio is True or rpio == 1):
    servo = GPIO.PWM.Servo()  # PWM module uses servo everywhere, so we do to

    def pwm(pin, state):
        if state == 0:
            print("servo.stop_servo(pin)")
        elif state > 0 and state <= 1:
            tmp_var = state * 20000
            print("servo.set_servo(pin, tmp_var)")
        else:
            print("Error: value not recognised, please make sure it is between 0 and 1.")
else:
    def pwm(pin, state):
        if state >= 0.5:
            print("GPIO.output(pin, 1)")
        elif state < 0.5:
            print("GPIO.output(pin, 0)")
        else:
            print("Error: value not recognised, please make sure it is between 0 and 1.")


def updown(thrust, air_time):  # Thrust is a value between 0 and 1
    if 0 <= thrust <= 1:
        print("pwm(updown_pin, 1)")
        time.sleep(air_time)
        print("pwm(updown_pin, 0)")
    else:
        print("Error1")
    return


def leftright(direction, air_time):
    if direction == "left":
        print("GPIO.output(updown_pin, 1)")
        print("GPIO.output(neutral_pin, 0)")
        time.sleep(air_time)
        print("GPIO.output(neutral_pin, 1)")
        print("GPIO.output(updown_pin, 0)")
    elif direction == "right":
        print("GPIO.output(updown_pin, 1)")
        print("GPIO.output(neutral_pin, 0)")
        print("GPIO.output(right_pin, 1)")
        time.sleep(air_time)
        print("GPIO.output(right_pin, 0)")
        print("GPIO.output(neutral_pin, 1)")
        print("GPIO.output(updown_pin, 0)")
    else:
        print("Error2")
    return


def forwardbackward(direction, air_time):
    if direction == "forward":
        print("GPIO.output(updown_pin, 1)")
        print("GPIO.output(stationary_pin, 0)")
        time.sleep(air_time)
        print("GPIO.output(stationary_pin, 1)")
        print("GPIO.output(updown_pin, 0)")
    elif direction == "backward":
        print("GPIO.output(updown_pin, 1)")
        print("GPIO.output(stationary_pin, 0)")
        print("GPIO.output(backward_pin, 1)")
        time.sleep(air_time)
        print("GPIO.output(backward_pin, 0)")
        print("GPIO.output(stationary_pin, 1)")
        print("GPIO.output(updown_pin, 0)")
    else:
        print("Error3")
    return

error = 0

while True:
    user_input = input("You have the following options: up, left/right, forward/backward and exit, default air time is 5 seconds.").lower()
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
        error = error + 1
        if error >= 3:
            print("Too many errors occured, exiting now.")
            break
        print("An error occured, please try again and check your spelling.")

print("GPIO.cleanup()")
exit()
