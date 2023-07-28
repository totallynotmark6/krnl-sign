from time import sleep
from krnl_sign.screen import init_matrix, update_screen
from krnl_sign.updater import update, update_exists


if __name__ == "__main__":
    init_matrix()
    counter = 0
    while True:
        update_screen()
        sleep(1)
        counter += 1
        counter %= 60
        if counter == 0:
            if update_exists():
                success = update()
                if success:
                    exit(5) # exit with code 5 to indicate that the program should be restarted...?

    sleep(5)