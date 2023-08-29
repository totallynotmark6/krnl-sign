from datetime import timedelta

import arrow
from krnl_sign.base_task import RepeatingTask
from krnl_sign.consts import DEV_MODE
from krnl_sign.update import check_for_updates


class UpdateTask(RepeatingTask):
    def __init__(self):
        if DEV_MODE:
            super().__init__(timedelta(minutes=15))
        else:
            super().__init__(timedelta(days=1))
            self.last_run = arrow.now().replace(hour=0, minute=5, second=0, microsecond=0) # run just after midnight
    
    def on_run(self):
        if check_for_updates():
            exit(5)

class UpdateWeather(RepeatingTask):
    def __init__(self):
        super().__init__(timedelta(hours=1))
        self.on_run()
    
    def on_run(self):
        pass
