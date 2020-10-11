import smbus
import numpy as np
from typing import Tuple


# Addresses
#https://github.com/adafruit/Adafruit_TCS34725/blob/master/Adafruit_TCS34725.h

#bus Initialization
bus = smbus.SMBus(2)

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
B_MS = 0x1B  # Blue channel data high by


def read_data(register):
    return bus.read_byte_data(I2C_ADDRESS, register)


def get_raw_color_value(ls, ms):
    """
    ls: Least sig bit of the color address
    ms: Most sig bit of the color address
    """
    msb = read_data(ms) << 8
    lsb = read_data(ls)
    return np.int16(msb | lsb)

def convert_raw_to_rgb(red, green, blue, clear):
    """
    Pass the raw values from the TCS to this function to convert to rgb values.
    Returns tuple of red, green, blue values
    """
    # avoid division by zero when reading black color
    if clear == 0:
        return (0, 0, 0)

    return (
        red / sum * 255.0,
        green / sum * 255.0,
        blue / sum * 255.0,
    )

if __name__ == "__main__":
    # https://github.com/adafruit/Adafruit_TCS34725/blob/6dc42834bd071aeb94bdddff7e17cb662de20ad2/Adafruit_TCS34725.h#L53
    WAKE_UP_VALUE = 1
    WAKE_UP_ADDRESS = 0x01
    #Power on the Sensor
    bus.write_byte_data(I2C_ADDRESS, WAKE_UP_ADDRESS, WAKE_UP_VALUE)

    while True:
        # Read the raw color data
        r = get_raw_color_value(R_LS, R_MS)
        g = get_raw_color_value(G_LS, G_MS)
        b = get_raw_color_value(B_LS, B_MS)
        clear = get_raw_color_value(CD_LS, CD_MS)

        # Convert the raw data to actual rgb
        r, g, b = convert_raw_to_rgb(r, g, b, clear)

        # Print
        print(f"Red: {r} Green: {g} Blue: {b}")
