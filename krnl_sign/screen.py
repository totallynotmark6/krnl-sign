from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions

_matrix = None

def init_matrix():
    global _matrix
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.disable_hardware_pulsing = True
    _matrix = RGBMatrix(options = options)
    _matrix.SetPixel(0, 0, 255, 255, 255)
