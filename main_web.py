#!/usr/bin/env pybricks-micropython
from microWebSrv import MicroWebSrv

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
    return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]

def clamp(value, minn, maxn):
    return max(min(maxn, value), minn)

@MicroWebSrv.route('/clev3r/control', 'POST')
def _httpHandlerPost(httpClient, httpResponse):
    formData = httpClient.ReadRequestPostedFormData()
    action = formData["action"]
    data = formData["data"]

    if action == 'speed':
        speed = clamp(int(data), -100, 100)
        # Set motor voltages. 
        left_motor.dc(-speed)
        right_motor.dc(-speed)
        content = "OK"
        httpResponse.WriteResponseJSONOk(content)
    elif action == 'steer':
        angle = clamp(int(data), -40, 40)
        steer_motor.track_target(angle)
        content = "OK"
        httpResponse.WriteResponseJSONOk(content)
    else:
        content = "Failure" 
        httpResponse.WriteResponseJSONError(content)

@MicroWebSrv.route('/clev3r/control', 'GET')
def _httpHandlerGet(httpClient, httpResponse):
    	content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
        	<meta charset="UTF-8" />
            <title>CLEV3R CAR</title>
        </head>
        <body>
            <h1>CLEV3R CAR</h1>
        </body>
    </html>
	"""
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = content )


srv = MicroWebSrv(port=8081, webPath='html/')
print("starting")
srv.Start()


