"""
Adapted from https://github.com/adafruit/Adafruit_CircuitPython_SSD1306/blob/master/examples/ssd1306_framebuftest.py
and https://github.com/adafruit/Adafruit_CircuitPython_PN532/blob/master/examples/pn532_simpletest.py
"""

import board
import busio
import time
from digitalio import DigitalInOut

import adafruit_ssd1306

from adafruit_pn532.spi import PN532_SPI

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

# PN532 SPI connection:
pn_cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, pn_cs_pin, debug=False)

# OLED ssd 1306 SPI connection:
ssd1306_cs_pin = DigitalInOut(board.D24)
ssd1306_dc_pin = DigitalInOut(board.D25)
ssd1306_reset_pin = DigitalInOut(board.D23)
WIDTH = 128
HEIGHT = 32

display = adafruit_ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, ssd1306_dc_pin, ssd1306_reset_pin, ssd1306_cs_pin)

"""
 OLED painting
"""
print("Lines test")
# we'll draw from corner to corner, lets define all the pair coordinates here
corners = ((0, 0), (0, display.height-1), (display.width-1, 0),
           (display.width-1, display.height-1))

display.fill(0)
for corner_from in corners:
    for corner_to in corners:
        display.line(corner_from[0], corner_from[1],
                     corner_to[0], corner_to[1], 1)
display.show()
time.sleep(1)
display.poweroff()

"""
 PNC setup and loop
"""
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

print('Waiting for RFID/NFC card...')
while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    print('.', end="")
    # Try again if no card is available.
    if uid is None:
        continue
    print('Found card with UID:', [hex(i) for i in uid])
