import requests
from krnl_sign.radioco_data import is_live
from krnl_sign.screen_tasks.now_playing import KRNLNowPlaying
from krnl_sign.screen_tasks.psa import RandomPSA, SelectPSA, ShowsAndCounting, Slogan


class ScreenManager:
    def __init__(self):
        self.live_tasks = []
        self.not_live_tasks = []
        self.current_task = None
        self.index = 0

    @property
    def current_tasks(self):
        if is_live():
            return self.live_tasks
        return self.not_live_tasks

    def update_tasks(self):
        live_req = requests.get("https://raw.githubusercontent.com/KRNL-Radio/data-sink/main/sign/live_layout.json")
        not_live_req = requests.get("https://raw.githubusercontent.com/KRNL-Radio/data-sink/main/sign/not_live_layout.json")
        self.live_tasks = parse_tasks(live_req.json())
        self.not_live_tasks = parse_tasks(not_live_req.json())
        # self.not_live_tasks = [
        #     # put tasks here!
        #     # ScreenTask(timedelta(seconds=10), timedelta(seconds=15)),
        #     # Slogan(),
        #     ShowsAndCounting()
        # ]
        pass

    def override_current_task(self, task):
        if self.current_task:
            self.current_task.teardown(True)
        self.current_task = task
        self.current_task.prepare()
        self.index = -1

    def draw(self, canvas, delta_time):
        if not self.current_task:
            if self.index >= len(self.current_tasks):
                self.index = 0
            self.current_task = self.current_tasks[self.index]
            if not self.current_task.prepare():
                # uh... we don't want to do anything!
                # so let's just skip this task!
                self.current_task = None
                self.index += 1
                if self.index >= len(self.current_tasks):
                    self.index = 0
                return self.draw(canvas, delta_time)
        if self.current_task.draw(canvas, delta_time):
            self.current_task.teardown()
            self.current_task = None
            self.index += 1
            return True
        return False

def parse_tasks(json):
    result = []
    for task in json['screens']:
        if task['type'] == 'random_psa':
            result.append(RandomPSA.construct_from_config({}))
        elif task['type'] == 'select_psa':
            result.append(SelectPSA.construct_from_config(task))
        elif task['type'] == 'slogan':
            result.append(Slogan.construct_from_config({}))
        elif task['type'] == 'krnl_now_playing':
            result.append(KRNLNowPlaying.construct_from_config({}))
        elif task['type'] == 'shows_and_counting':
            result.append(ShowsAndCounting.construct_from_config({}))
        # elif task['type'] == 'something_else':
        #     result.append(SomethingElse.construct_from_config(task))
        else:
            print("Unknown task type: {}".format(task['type']))
    return result
        