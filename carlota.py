
import time
import board
import maze
import displayio
import random
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
palette[3] = 0x003870  # dark blue
palette[4] = 0xfcb4c4  # light pink
palette[5] = 0x85FF00  # greenish
palette[6] = 0xfcb4c4
palette[7] = 0xFFFFFF  # white


# --- Drawing setup ---

bitmap = displayio.Bitmap(64, 64, 8)
grid = displayio.TileGrid(bitmap, pixel_shader=palette)

group = displayio.Group()
group.append(grid)

matrix = Matrix(width=64, height=64)
matrix.display.show(group)

 # --- Choosing a Random Cell ---

x = random.randint(1,62)
y = random.randint(1,62)

cell = bitmap[x, y]

# --- Choosing a Random Color for the Cell ---

color = random.randint(1,2)
bitmap[x, y] = color

# --- Creating an Array for the surrounding cells ---

#def array(surrounding_cells, x, y):
    #array = np.array(surrounding_cells)

    #return array

#surrounding_cells = bitmap[[[x-1,y-1],[x-1,y],[x-1,y+1]],
  #                   [[x,y-1],[x,y],[x,y+1]],
   #                  [[x+1,y-1],[x+1,y],[x+1,y+1]]]

#first_array = array(surrounding_cells)

# --- Determining Surrounding of Cell ---

#def surrounding()

#cells_alive = np.sum(surrounding_cells[x-1:x+1, y-1:y+1] - surrounding_cells[x,y])
#if surrounding_cells[x,y] == 1 and cells_alive < 2 or cells_alive > 3:
    #cell turns off


while True:
    time.sleep(1)

