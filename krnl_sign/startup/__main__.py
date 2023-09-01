try:
    from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
    RUNNING_ON_EMULATOR = False
except ImportError:
    from RGBMatrixEmulator import graphics, RGBMatrix, RGBMatrixOptions
    RUNNING_ON_EMULATOR = True

from datetime import timedelta
import os
import pwd
from time import sleep
import arrow
from krnl_sign.consts import COLOR_BLUE, COLOR_GRAY, COLOR_MINT, COLOR_PURPLE, COLOR_RED, COLOR_WHITE, FONT_4x6, FONT_5x7
from threading import Thread
from random import choice
import subprocess

from krnl_sign.run_with_user import run_with_user

_matrix = None
_canvas = None
loading_splashes = [
    "Baking ice cream",
    "Loading!",
    "Dividing by zero",
    "Working hard...",
    "Hardly working...",
    "Updating Updater",
    "Proving P=NP...",
    "Burning CDs",
    "Baking cookies!",
]
loading_splash = choice(loading_splashes)

def init_matrix():
    global _matrix, _canvas
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.disable_hardware_pulsing = True
    # options.gpio_slowdown = ???
    _matrix = RGBMatrix(options = options)
    _canvas = _matrix.CreateFrameCanvas()

class UpdateThread(Thread):
    def run(self) -> None:
        if RUNNING_ON_EMULATOR:
            print("Running on emulator, skipping update (after a bit...)")
            sleep(5)
            return
        print("Updating...")
        proc = run_with_user(["git", "pull"], "krnl")
        if proc.returncode != 0:
            print("Error updating git!")
            return
        py_proc = subprocess.run(["python3", "-m", "pip", "install", "-e", "."])
        if py_proc.returncode != 0:
            print("Error updating dependencies!")
            return
        print("Done updating!")

def update_screen(elapsed_time: timedelta, finished=False):
    global _matrix, _canvas

    canvas = _canvas
    canvas.Clear()

    _matrix.brightness = 100

    # draw!
    graphics.DrawText(canvas, FONT_4x6, 0, 5, COLOR_WHITE, "KRNL Sign")
    timestr = str(round(elapsed_time.total_seconds())).rjust(16)
    graphics.DrawText(canvas, FONT_4x6, 0, 32, COLOR_GRAY, timestr)
    if finished:
        graphics.DrawText(canvas, FONT_4x6, 0, 20, COLOR_RED, "Finished!")
    else:
        graphics.DrawText(canvas, FONT_4x6, 0, 20, COLOR_BLUE, loading_splash)

    _canvas = _matrix.SwapOnVSync(canvas)

def clear_canvas():
    global _canvas, _matrix
    _canvas.Clear()
    graphics.DrawText(_canvas, FONT_4x6, 0, 5, COLOR_GRAY, " Made w/    by")
    graphics.DrawText(_canvas, FONT_4x6, 0, 5, COLOR_RED,  "         <3   ")
    graphics.DrawText(_canvas, FONT_4x6, 0, 19, COLOR_MINT,"totallynotmark6".center(16))
    graphics.DrawText(_canvas, FONT_4x6, 0, 26, COLOR_PURPLE,"KRNL Radio".center(16))
    graphics.DrawText(_canvas, FONT_4x6, 0, 32, COLOR_RED,"C4".center(16))
    _canvas = _matrix.SwapOnVSync(_canvas)
    sleep(.5)

def main():
    init_matrix()
    ut = UpdateThread()
    ut.start()
    start = arrow.now()
    while ut.is_alive():
        time_elapsed = arrow.now() - start
        update_screen(time_elapsed)
    time_elapsed = arrow.now() - start
    update_screen(time_elapsed, True)
    sleep(2)
    clear_canvas()
    print("Done!")


if __name__ == "__main__":
    main()
