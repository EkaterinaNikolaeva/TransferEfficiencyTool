from abc import ABC


class Target(ABC):
    def start(self) -> None:
        pass

    def finish(self) -> float:
        pass
