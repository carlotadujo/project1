import time
import board
import maze
import displayio
import terminalio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from adafruit_matrixportal.network import Network
from adafruit_matrixportal.matrix import Matrix


# --- Color palette ---
palette = displayio.Palette(8)
palette[0] = 0x000000  # black
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


def get(y, x, scale=2, xoff=1, yoff=1):
    return bitmap[x * scale + xoff, y * scale + yoff]


def set(y, x, v, scale=2, xoff=1, yoff=1):
    bitmap[x * scale + xoff, y * scale + yoff] = v
    if scale==2:
        bitmap[x * scale + xoff, y * scale + yoff + 1] = v
        bitmap[x * scale + xoff + 1, y * scale + yoff] = v
        bitmap[x * scale + xoff + 1, y * scale + yoff + 1] = v


class GameOfLife:
    def __init__(self, width, height, initial_cells):
        self.width = width
        self.height = height
        self.initial_cells = initial_cells