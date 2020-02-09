import logging
logging.basicConfig(filename='plastic_player.log', format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

import board
import busio
import time
from digitalio import DigitalInOut
import binascii
from mopidy_client import play_new_tracks, stop_track
from tracks_model import get_track_uris

import adafruit_ssd1306
from adafruit_pn532.spi import PN532_SPI

logging.info('Starting up')

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

# PN532 SPI connection:
pn_cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, pn_cs_pin, debug=False)

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

current_tag = None
count_loops_without_tag = 0
COUNT_LOOPS_WITHOUT_TAG_TO_STOP = 4
print('Waiting for RFID/NFC card...')
while True:
    try:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)

        if uid is not None:
            tag = binascii.hexlify(uid).decode('ascii')
            if tag != current_tag:
                print('Found card with tag:', tag)
                current_tag = tag
                track_uris = get_track_uris(tag)
                if track_uris is not None:
                    play_new_tracks(track_uris)

        # Try again if no card is available.
        if uid is None:
            count_loops_without_tag += 1
            if (count_loops_without_tag >= COUNT_LOOPS_WITHOUT_TAG_TO_STOP):
                count_loops_without_tag = 0
                current_tag = None
                stop_track()

    except Exception:
        logging.error(traceback.print_exc())
        print(traceback.print_exc())
