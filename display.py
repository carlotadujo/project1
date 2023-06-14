import time
import board
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

class Display:
    def __init__(self, scale=1, x_offset=0, y_offset=0):
        self.scale = scale
        self.x_offset = x_offset
        self.y_offset = y_offset

    def get(self, x, y):
        x, y = xy
        return bitmap[y * self.scale + self.y_offset, x * self.scale + self.x_offset]

    def set(self, x, y, v):
        bitmap[y * self.scale + self.y_offset, x * self.scale + self.x_offset] = v
        if self.scale == 2:
            bitmap[y * self.scale + self.y_offset, x * self.scale + self.x_offset + 1] = v
            bitmap[y * self.scale + self.y_offset, x * self.scale + 1] = v
            bitmap[y * self.scale + self.y_offset + 1, x * self.scale + 1] = v