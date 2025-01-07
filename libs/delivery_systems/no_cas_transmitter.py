from abc import ABC


class NoCasTransmitter(ABC):
    def preprocess(self, source):
        pass

    def deliver(self, source, output):
        pass
