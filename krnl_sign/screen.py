from time import sleep
import arrow
from pkg_resources import resource_filename
try:
    from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
except ImportError:
    from RGBMatrixEmulator import graphics, RGBMatrix, RGBMatrixOptions

_matrix = None

COLOR_WHITE = graphics.Color(255, 255, 255)
COLOR_RED = graphics.Color(255, 69, 58)
COLOR_ORANGE = graphics.Color(255, 159, 10)
COLOR_YELLOW = graphics.Color(255, 214, 10)
COLOR_GREEN = graphics.Color(50, 215, 75)
COLOR_MINT = graphics.Color(102, 212, 207)
COLOR_TEAL = graphics.Color(106, 196, 220)
COLOR_CYAN = graphics.Color(90, 200, 245)
COLOR_BLUE = graphics.Color(10, 132, 255)
COLOR_INDIGO = graphics.Color(94, 92, 230)
COLOR_PURPLE = graphics.Color(191, 90, 242)
COLOR_PINK = graphics.Color(255, 55, 95)
COLOR_BROWN = graphics.Color(172, 142, 104)
COLOR_GRAY = graphics.Color(152, 152, 157)

FONT_4x6 = graphics.Font()
FONT_4x6.LoadFont(resource_filename(__name__, "fonts/4x6.bdf"))
FONT_5x7 = graphics.Font()
FONT_5x7.LoadFont(resource_filename(__name__, "fonts/5x7.bdf"))

def init_matrix():
    global _matrix
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.disable_hardware_pulsing = True
    _matrix = RGBMatrix(options = options)
    # _matrix.SetPixel(0, 0, 255, 255, 255)

def draw_header(canvas):
    now = arrow.now()
    current_time = now.format("hh:mm")
    current_date = now.format("ddd,MMM D")
    graphics.DrawLine(canvas, 0, 7, 63, 7, COLOR_GRAY)
    graphics.DrawLine(canvas, 21, 0, 21, 7, COLOR_GRAY)
    graphics.DrawText(canvas, FONT_4x6, 1, 6, COLOR_PURPLE, current_time)
    graphics.DrawText(canvas, FONT_4x6, 23, 6, COLOR_PURPLE, current_date)

def draw_live(canvas):
    # draw in center of screen
    draw_rect(canvas, 21, 10, 21, 8, COLOR_RED)
    graphics.DrawText(canvas, FONT_5x7, 22, 17, COLOR_WHITE, "LIVE")
    graphics.DrawText(canvas, FONT_5x7, 32 - 25, 27, COLOR_WHITE, "Mark Smith")

def draw_rect(canvas, x, y, w, h, color):
    # use Canvas.SetPixel() to fill
    for i in range(w):
        for j in range(h):
            canvas.SetPixel(x + i, y + j, color.red, color.green, color.blue)

def update_screen():
    global _matrix
    canvas = _matrix.CreateFrameCanvas()
    draw_header(canvas)
    now = arrow.now()
    if now.minute % 2 == 0: # temporary!~
        draw_live(canvas)
    _matrix.SwapOnVSync(canvas)

