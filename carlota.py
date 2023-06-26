
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
#duplicate coordinates, run again

def random_population(min=100, max=100):
    for i in range(random.randint(min,max)):
        x = random.randint(1,62)
        y = random.randint(1,62)
        bitmap[x, y] = 1



# --- Random Patterns ---

def glider(row, column):
        glider_pattern1 = [
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1]]

        for i in range(len(glider_pattern1)):
            for j in range(len(glider_pattern1[i])):
                bitmap[row + i, column + j] = glider_pattern1[i][j]

def blinker(row, column):
        blinker = [1, 1, 1]

        for i in range(len(blinker)):
            bitmap[row+i, column] = blinker[i]
            if blinker[i] == 1:
                bitmap[row+i, column] = 1


def glider2(row, column):
        glider_pattern2 = [
        [1, 0, 0],
        [0, 1, 1],
        [1, 1, 0]]

        for i in range(len(glider_pattern2)):
            for j in range(len(glider_pattern2[i])):
                bitmap[row + i, column + j] = glider_pattern2[i][j]

def toad(row, column):
        toad = [
        [1, 1, 1, 0],
        [0, 1, 1, 1]]

        for i in range(len(toad)):
            for j in range(len(toad[i])):
                bitmap[row + i, column + j] = toad[i][j]

def static(row, column):
        static = [
        [1, 1, 0],
        [1, 0, 1],
        [0, 1, 0]]

        for i in range(len(static)):
            for j in range(len(static[i])):
                bitmap[row + i, column + j] = static[i][j]


#random_population(90,200)

row = random.randint(1,62)
column = random.randint(1,62)
blinker(row, column)

row = random.randint(1,62)
column = random.randint(1,62)
glider(row, column)

row = random.randint(1,62)
column = random.randint(1,62)
glider2(row, column)

row = random.randint(1,62)
column = random.randint(1,62)
toad(row, column)

row = random.randint(1,62)
column = random.randint(1,62)
static(row, column)

while True:
    time.sleep(1)

