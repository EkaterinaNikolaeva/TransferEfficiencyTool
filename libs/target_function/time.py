from libs.target_function.target import Target
import time


class Time(Target):
    def start(self) -> None:
        self.start_time = time.time()

    def finish(self) -> float:
        return time.time() - self.start_time
