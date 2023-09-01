
from krnl_sign.screen import init_matrix, update_screen
from krnl_sign.tasks import TaskManager

def main():
    init_matrix()
    tm = TaskManager()
    
    while True:
        tm.check_and_run_tasks()
        update_screen()


if __name__ == "__main__":
    main()