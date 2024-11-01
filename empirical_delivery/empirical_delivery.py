from abc import ABC


class EmpiricalDelivery(ABC):
    def make_chunking(self, source, chunk_size="16:64:256"):
        pass

    def deliver(self):
        pass
