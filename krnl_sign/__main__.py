from time import sleep
from krnl_sign.screen import clear_matrix, init_matrix, update_screen


if __name__ == "__main__":
    init_matrix()
    try:
        while True:
            update_screen()
    finally:
        print('hi')
        clear_matrix()


    sleep(5)