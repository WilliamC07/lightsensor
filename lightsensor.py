import smbus
import numpy as np
from typing import Tuple


# Addresses
#https://github.com/adafruit/Adafruit_TCS34725/blob/master/Adafruit_TCS34725.h

#bus Initialization
bus = smbus.SMBus(2)

# Command flag
COMMAND = 0b10000000

#LightSensor I2C_Address
I2C_ADDRESS = 0x29

#Relevant Registers (From .h sheet)
CD_LS = 0x14  # Clear channel data low byte 
CD_MS = 0x15  # Clear channel data high byte
R_LS = 0x16  # Red channel data low byte 
R_MS = 0x17  # Red channel data high byte 
G_LS = 0x18  # Green channel data low byte 
G_MS = 0x19  # Green channel data high byte 
B_LS = 0x1A  # Blue channel data low byte 
B_MS = 0x1B  # Blue channel data high byte

# https://github.com/adafruit/Adafruit_TCS34725/blob/master/Adafruit_TCS34725.cpp
# https://github.com/adafruit/Adafruit_TCS34725/blob/master/Adafruit_TCS34725.h
# http://wiki.erazor-zone.de/wiki:linux:python:smbus:doc

# todo:
# 1. fix read byte data to write to command address
# 2. Make it read two bytes 

def read_data(register):
    return bus.read_byte_data(I2C_ADDRESS, COMMAND | register)


def get_raw_color_value(ls):
    """
    ls: Least sig bit of the color address
    ms: Most sig bit of the color address
    """
    lsb = read_data(ls)
    return np.int16(lsb)

def convert_raw_to_rgb(red, green, blue, clear):
    """
    Pass the raw values from the TCS to this function to convert to rgb values.
    Returns tuple of red, green, blue values
    """
    # avoid division by zero when reading black color
    if clear == 0:
        return (0, 0, 0)

    return (
        red / clear * 255.0,
        green / clear * 255.0,
        blue / clear * 255.0,
    )

if __name__ == "__main__":
    # https://github.com/adafruit/Adafruit_TCS34725/blob/6dc42834bd071aeb94bdddff7e17cb662de20ad2/Adafruit_TCS34725.h#L53
    #Power on the Sensor (take out of sleep mode) (page 8,15)
    PON = 0x00
    bus.write_byte_data(I2C_ADDRESS, PON, 1)
    
    # Activates the RGBC (turn on sensor to read color) (15)
    AEN = 0x02
    bus.write_byte_data(I2C_ADDRESS, AEN, 1)

    # Set the integration cycle to highest for most accurate reading (page 16)
    ATIME = 0x01
    bus.write_byte_data(I2C_ADDRESS, ATIME, 0x00)

    while True:
        # Read the raw color data
        r = get_raw_color_value(R_LS)
        g = get_raw_color_value(G_LS)
        b = get_raw_color_value(B_LS)
        clear = get_raw_color_value(CD_LS)

        # Convert the raw data to actual rgb
        r, g, b = convert_raw_to_rgb(r, g, b, clear)

        # Print
        print("Red: {} Green: {} Blue: {}".format(r, g, b))
