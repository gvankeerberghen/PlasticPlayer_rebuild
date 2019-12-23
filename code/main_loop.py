"""
Adapted from https://github.com/adafruit/Adafruit_CircuitPython_SSD1306/blob/master/examples/ssd1306_framebuftest.py
and https://github.com/adafruit/Adafruit_CircuitPython_PN532/blob/master/examples/pn532_simpletest.py
"""

import logging
logging.basicConfig(filename='plastic_player.log', format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import board
import busio
import time
from digitalio import DigitalInOut
import binascii
from mopidy_client import play_new_track, stop_track
from tracks_model import get_track_uri

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
# We'll draw from corner to corner, lets define all the pair coordinates here
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

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

current_tag = None
count_loops_without_tag = 0
COUNT_LOOPS_WITHOUT_TAG_TO_STOP = 4
print('Waiting for RFID/NFC card...')
while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)

    if uid is not None:
        tag = binascii.hexlify(uid).decode('ascii')
        if tag != current_tag:
            print('Found card with tag:', tag)
            current_tag = tag
            track_uri = get_track_uri(tag)
            if track_uri is not None:
                play_new_track(track_uri)

    # Try again if no card is available.
    if uid is None:
        count_loops_without_tag += 1
        if (count_loops_without_tag >= COUNT_LOOPS_WITHOUT_TAG_TO_STOP):
            count_loops_without_tag = 0
            current_tag = None
            stop_track()
