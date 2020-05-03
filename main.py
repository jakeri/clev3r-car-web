#!/usr/bin/env pybricks-micropython
 
# from pybricks import ev3brick as brick
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
 
import struct
 
# Declare motors 
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
steer_motor = Motor(Port.D)
forward = 0
left = 0
 
# A helper function for converting stick values (0 - 255)
# to more usable numbers (-100 - 100)
def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
 
    val: float or int
    src: tuple
    dst: tuple
 
    example: print(scale(99, (0.0, 99.0), (-1.0, +1.0)))
    """
    return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]
 
 
# Find the PS3 Gamepad:
# /dev/input/event3 is the usual file handler for the gamepad.
# look at contents of /proc/bus/input/devices if it doesn't work.
infile_path = "/dev/input/event4"
# open file in binary mode
in_file = open(infile_path, "rb")
# Read from the file
# long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llHHI'    
EVENT_SIZE = struct.calcsize(FORMAT)
event = in_file.read(EVENT_SIZE)

print("started")
while event:
    (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)
    if ev_type == 1:
        if code == 304:
            brick.sound.beep(500, 500)
        if code == 305:
            print("Bye bye")
            break
    # Type 1 event - buttons
        # Code 304 - X
        # Code 308 - Square
        # Code 307 - Triangle
        # Code 305 - Circle
        # Code 318 - right stick pressed
        # Code 317 - l stick pressed
        # Code 310 - L1 trigger
        # Code 311 - R1 trigger
        # Code 314 - Share button
        # Code 315 - Options button
        # Code 316 - PS button
    elif ev_type == 3:
    # Type 3 event - sticks
        # Code 3 - right stick horizontal
        # Code 2 - L2 trigger
        # Code 5 - R2 trigger
        # Code 0 - left stick horizontal (left is 0)
        # Code 1 - left stick vertical (forward is 0)
        # Code 4 - r stick vertical
        # Code 17 - dpad vertical
        # Code 16 - dpad horizontal
        if code == 3:
            left = scale(value, (0,255), (40, -40))
        if code == 1: # Righ stick vertical
            forward = scale(value, (0,255), (100,-100))
        
    # Set motor voltages. 
    left_motor.dc(-forward)
    right_motor.dc(-forward)
 
    # Track the steering angle
    steer_motor.track_target(left)
 
    # Finally, read another event
    event = in_file.read(EVENT_SIZE)
 
in_file.close()