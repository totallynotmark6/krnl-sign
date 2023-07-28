from time import sleep
from krnl_sign.screen import init_matrix, update_screen


if __name__ == "__main__":
    init_matrix()
    while True:
        update_screen()
        sleep(1)


    sleep(5)