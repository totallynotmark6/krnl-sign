import sys
from time import sleep
import arrow
from datetime import timedelta
from pkg_resources import resource_filename

from krnl_sign.radioco_data import get_live_data, is_live
try:
    from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
except ImportError:
    from RGBMatrixEmulator import graphics, RGBMatrix, RGBMatrixOptions

_matrix = None
_canvas = None
_frame_count = 0
_last_update = arrow.now()
_start_time = arrow.now()

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
    global _matrix, _canvas
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.disable_hardware_pulsing = True
    # options.gpio_slowdown = ???
    _matrix = RGBMatrix(options = options)
    _canvas = _matrix.CreateFrameCanvas()
    # _matrix.SetPixel(0, 0, 255, 255, 255)

def clear_matrix():
    global _matrix
    if _matrix is not None:
        _matrix.Clear()

def draw_header(canvas):
    now = arrow.now()
    current_time = now.format("h:mm").rjust(5)
    current_date = now.format("ddd,MMM D")
    graphics.DrawLine(canvas, 0, 7, 63, 7, COLOR_GRAY)
    graphics.DrawLine(canvas, 21, 0, 21, 7, COLOR_GRAY)
    graphics.DrawText(canvas, FONT_4x6, 1, 6, COLOR_PURPLE, current_time)
    graphics.DrawText(canvas, FONT_4x6, 23, 6, COLOR_PURPLE, current_date)

def draw_headline_and_msg(canvas, headline, msg, headline_bg_color, msg_color, headline_fg_color=COLOR_WHITE, MSG_FONT=FONT_5x7, HEADLINE_FONT=FONT_5x7):
    headline_width = sum([HEADLINE_FONT.CharacterWidth(ord(c)) or HEADLINE_FONT.CharacterWidth(ord("a")) for c in headline])
    msg_width = sum([MSG_FONT.CharacterWidth(ord(c)) or MSG_FONT.CharacterWidth(ord("a")) for c in msg])
    if headline_width > 64 or msg_width > 64:
        print("ERROR: text too long")
        return draw_headline_and_msg(canvas, "Sign Error", "Text too long", None, COLOR_WHITE, COLOR_RED, FONT_4x6)
    headline_x = 32 - (headline_width // 2)
    msg_x = 32 - (msg_width // 2)
    if headline_bg_color:
        draw_rect(canvas, headline_x - 1, 10, headline_width + 1, HEADLINE_FONT.height + 1, headline_bg_color)
    graphics.DrawText(canvas, HEADLINE_FONT, headline_x, 17, headline_fg_color, headline)
    graphics.DrawText(canvas, MSG_FONT, msg_x, 27, msg_color, msg)

def draw_progress(canvas, progress, color=COLOR_RED):
    draw_rect(canvas, 1, 13, 62, 6, COLOR_WHITE, False)
    progress = max(0, min(1, progress))
    if progress > 0:
        draw_rect(canvas, 2, 14, int(60 * progress), 4, color, True)

def draw_spinner(canvas, spinner, frame_counter=0, color=COLOR_RED):
    font = FONT_5x7
    spinner_frame = spinner["frames"][frame_counter % len(spinner["frames"])]
    spinner_delay = spinner["interval"] / 1000
    # print(spinner_frame, ord(spinner_frame))
    spinner_width = sum([font.CharacterWidth(ord(c)) or font.CharacterWidth(ord(a)) for c in spinner_frame])
    spinner_x = 32 - (spinner_width // 2)
    graphics.DrawText(canvas, font, spinner_x, 16, color, spinner_frame)
    sleep(spinner_delay)

def draw_rect(canvas, x, y, w, h, color, fill=True):
    # use Canvas.SetPixel() to fill
    if fill:
        for i in range(h):
            graphics.DrawLine(canvas, x, y + i, x + w - 1, y + i, color)
    else:
        graphics.DrawLine(canvas, x, y, x + w - 1, y, color)
        graphics.DrawLine(canvas, x, y, x, y + h - 1, color)
        graphics.DrawLine(canvas, x + w - 1, y, x + w - 1, y + h - 1, color)
        graphics.DrawLine(canvas, x, y + h - 1, x + w - 1, y + h - 1, color)

def screen_active():
    now = arrow.now()
    # if is_summer():
    if True:
        # summer time! between 6 am and 8 pm.
        return now.hour >= 6 and now.hour < 20
    else:
        # normal hours! between 6 am and midnight.
        return now.hour >= 6 and now.hour < 24

def update_screen():
    global _matrix, _canvas, _frame_count, _last_update, _start_time
    
    now = arrow.now()
    delta_t = now - _last_update
    _last_update = now
    _time_elapsed_since_start = now - _start_time
    
    # watchdog
    if delta_t > timedelta(seconds=1):
        print("WARNING: update_screen() called after {} seconds".format(delta_t.seconds), file=sys.stderr)
    if delta_t > timedelta(seconds=30):
        print("ERROR: update_screen() called after {} seconds".format(delta_t.seconds), file=sys.stderr)
        exit(5)
    
    # clear canvas
    canvas = _canvas
    canvas.Clear()

    # brightness
    if screen_active():
        _matrix.brightness = 100
    else:
        _matrix.brightness = 0
        _canvas = _matrix.SwapOnVSync(canvas)
        return # don't draw anything!

    draw_header(canvas)
    # if is_live():
    #     draw_headline_and_msg(canvas, "LIVE", "Hello World!", COLOR_RED, COLOR_WHITE)
    # else:
    #     draw_headline_and_msg(canvas, "NOT LIVE", "a", COLOR_BLUE, COLOR_WHITE)
    draw_headline_and_msg(canvas, str(_time_elapsed_since_start), str(delta_t), None, COLOR_WHITE, COLOR_BLUE, FONT_4x6, FONT_4x6)
    
    # update the screen~
    _canvas = _matrix.SwapOnVSync(canvas)
    _frame_count += 1

