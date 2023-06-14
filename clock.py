# SPDX-FileCopyrightText: 2020 John Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Metro Matrix Clock
# Runs on Airlift Metro M4 with 64x32 RGB Matrix display & shield

import time
import board
import displayio
import terminalio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from adafruit_matrixportal.network import Network
from adafruit_matrixportal.matrix import Matrix

BLINK = True
DEBUG = False

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise
print("    Metro Minimal Clock")
print("Time will be set for {}".format(secrets["timezone"]))

import busio
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi
ESP32_CS = DigitalInOut(board.ESP_CS)
ESP32_READY = DigitalInOut(board.ESP_BUSY)
ESP32_RESET = DigitalInOut(board.ESP_RESET)
SPI = busio.SPI(board.SCK, board.MOSI, board.MISO)
ESP = adafruit_esp32spi.ESP_SPIcontrol(SPI, ESP32_CS, ESP32_READY, ESP32_RESET)

network = Network(status_neopixel=board.NEOPIXEL, debug=False, esp=ESP, external_spi=SPI)

# --- Color palette ---
palette = displayio.Palette(8)
palette[0] = 0x000000  # black background
palette[1] = 0xFF0000  # red
palette[2] = 0x00FF00  # green
palette[3] = 0x00FFFF  # blue
palette[4] = 0xCC4000  # amber
palette[5] = 0x85FF00  # greenish
palette[6] = 0xFFFF00
palette[7] = 0xFFFFFF  # white

# --- Drawing setup ---

bitmap = displayio.Bitmap(64, 64, 8)
grid = displayio.TileGrid(bitmap, pixel_shader=palette)

group = displayio.Group()
group.append(grid)

matrix = Matrix(width=64, height=64)
matrix.display.show(group)

if not DEBUG:
    font = bitmap_font.load_font("/IBMPlexMono-Medium-24_jep.bdf")
else:
    font = terminalio.FONT

label = Label(font)
group.append(label)  # add the clock label to the group


def update_time(*, hours=None, minutes=None, show_colon=False):
    now = time.localtime()  # Get the time values we need
    if hours is None:
        hours = now[3]
    if hours >= 18 or hours < 6:  # evening hours to morning
        label.color = palette[2]
    else:
        label.color = palette[4]  # daylight hours
    if hours > 12:  # Handle times later than 12:59
        hours -= 12
    elif not hours:  # Handle times between 0:00 and 0:59
        hours = 12

    if minutes is None:
        minutes = now[4]

    if BLINK:
        colon = ":" if show_colon or now[5] % 2 else " "
    else:
        colon = ":"

    label.text = "{hours}{colon}{minutes:02d}".format(
        hours=hours, minutes=minutes, colon=colon
    )
    bbx, bby, bbwidth, bbh = label.bounding_box
    # Center the label
    label.x = round(matrix.display.width / 2 - bbwidth / 2)
    label.y = matrix.display.height // 2
    if DEBUG:
        print("Label bounding box: {},{},{},{}".format(bbx, bby, bbwidth, bbh))
        print("Label x: {} y: {}".format(label.x, label.y))


last_check = None
update_time(show_colon=True)  # Display whatever time is on the board

while True:
    if last_check is None or time.monotonic() > last_check + 3600:
        try:
            update_time(
                show_colon=True
            )  # Make sure a colon is displayed while updating
            network.get_local_time()  # Synchronize Board's clock to Internet
            last_check = time.monotonic()
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)

    update_time()
    time.sleep(1)