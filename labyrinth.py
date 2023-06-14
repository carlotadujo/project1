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


def get(y, x, scale=2, xoff=1, yoff=1):
    return bitmap[x * scale + xoff, y * scale + yoff]


def set(y, x, v, scale=2, xoff=1, yoff=1):
    bitmap[x * scale + xoff, y * scale + yoff] = v
    if scale==2:
        bitmap[x * scale + xoff, y * scale + yoff + 1] = v
        bitmap[x * scale + xoff + 1, y * scale + yoff] = v
        bitmap[x * scale + xoff + 1, y * scale + yoff + 1] = v


PATH = 0
WALL = 4
THESEUS = 2
THREAD = 5
MINOTAUR = 1
VISITED = 3


def build_labyrinth(width, height, plan):
    for row in range(len(plan)):
        for col in range(len(plan[row])):
            if plan[row][col]:
                set(row, col, WALL)
            else:
                set(row, col, PATH)

    set(0, 1, THESEUS)
    set(width - 2, height - 2, MINOTAUR)


# def slay(y, x):
#     v = get(y, x)
#     if v == MINOTAUR:
#         return True
#     if v == WALL or v == VISITED:
#         return False

#     set(y, x, VISITED)

#     time.sleep(0.1)

#     if slay(y, x + 1):
#         return True
#     elif slay(y + 1, x):
#         return True
#     elif slay(y, x - 1):
#         return True
#     elif slay(y - 1, x):
#         return True
#     else:
#         return False


stack = []
def slay(y, x):
    stack.append((y, x))

    while len(stack):
        y, x = stack.pop()
        v = get(y, x)

        if v == MINOTAUR:
            return True
        elif v == WALL or v == VISITED:
            pass
        else:
            set(y, x, THESEUS)
            time.sleep(0.1)
            set(y, x, VISITED)

            stack.append((y - 1, x))
            stack.append((y, x - 1))
            stack.append((y + 1, x))
            stack.append((y, x + 1))


width, height, plan = maze.generate()
build_labyrinth(width, height, plan)
slay(0, 1)

while True:
    time.sleep(1)
