from datetime import timedelta
import arrow
import requests
import random
import json
import segno
import io
from krnl_sign.base_task import ScreenTask
from krnl_sign.consts import COLOR_PURPLE, COLOR_WHITE, FONT_4x6
from krnl_sign.util import requests_get_1hr_cache
try:
    from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
except ImportError:
    from RGBMatrixEmulator import graphics, RGBMatrix, RGBMatrixOptions

class RandomPSA(ScreenTask):
    psa: dict

    def __init__(self):
        super().__init__(suggested_run_time=timedelta(seconds=15))
    
    def prepare(self):
        req = requests_get_1hr_cache("https://raw.githubusercontent.com/KRNL-Radio/data-sink/main/sign/psa.json")
        self.psa = random.choice(req.json()['contents'])
        if self.psa['type'] == 'qr':
            self.suggested_run_time = timedelta(seconds=30) # can we do this dynamically?
            qr_code = segno.make_qr(self.psa['data'])
            buf = io.StringIO()
            qr_code.save(buf, kind='txt', border=0)
            self.qr_code = buf.getvalue().splitlines()
            if len(self.qr_code) > 25:
                print("QR code too big!")
                return False
        return super().prepare()

    def draw_frame(self, canvas, delta_time):
        if not self.psa['type'] == 'qr':
            self.draw_header(canvas)
            graphics.DrawText(canvas, FONT_4x6, 1, 15, COLOR_WHITE, self.psa['text'].center(16))
        else:
            now = arrow.now()
            current_time = now.format("h:mm").rjust(5)
            graphics.DrawText(canvas, FONT_4x6, 1, 32, COLOR_PURPLE, current_time)
            graphics.DrawText(canvas, FONT_4x6, 1, 6, COLOR_WHITE, self.psa['text'].center(16))
            current_line = 7
            for line in self.qr_code:
                current_x = 20
                for char in line:
                    if char == '0':
                        canvas.SetPixel(current_x, current_line, 255, 255, 255)
                    else:
                        canvas.SetPixel(current_x, current_line, 0, 0, 0)
                    current_x += 1
                current_line += 1

    @classmethod
    def construct_from_config(cls, config):
        return cls()
