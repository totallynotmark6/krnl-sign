from datetime import timedelta
import requests
import random
import json
from krnl_sign.base_task import ScreenTask
from krnl_sign.consts import COLOR_WHITE, FONT_4x6
try:
    from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
except ImportError:
    from RGBMatrixEmulator import graphics, RGBMatrix, RGBMatrixOptions

class RandomPSA(ScreenTask):
    psa: dict

    def __init__(self):
        super().__init__(suggested_run_time=timedelta(seconds=15))
    
    def prepare(self):
        req = requests.get("https://raw.githubusercontent.com/KRNL-Radio/data-sink/main/sign/psa.json")
        self.psa = random.choice(req.json()['contents'])
        return super().prepare()

    def draw_frame(self, canvas, delta_time):
        self.draw_header(canvas)
        graphics.DrawText(canvas, FONT_4x6, 1, 15, COLOR_WHITE, self.psa['text'])

    @classmethod
    def construct_from_config(cls, config):
        return cls()
