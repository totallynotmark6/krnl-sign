from time import sleep
import arrow
from pkg_resources import resource_filename
try:
    from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
except ImportError:
    from RGBMatrixEmulator import graphics, RGBMatrix, RGBMatrixOptions

_matrix = None
COLOR_WHITE = graphics.Color(255, 255, 255)
COLOR_GRAY = graphics.Color(128, 128, 128)

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
    graphics.DrawText(canvas, FONT_4x6, 1, 6, COLOR_WHITE, current_time)
    graphics.DrawText(canvas, FONT_4x6, 23, 6, COLOR_WHITE, current_date)

def update_screen():
    global _matrix
    canvas = _matrix.CreateFrameCanvas()
    draw_header(canvas)
    _matrix.SwapOnVSync(canvas)

