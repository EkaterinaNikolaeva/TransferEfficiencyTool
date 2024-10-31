from .empirical_delivery import EmpiricalDelivery


class Desync(EmpiricalDelivery):
    def __init__(self, chunk_size: str, cache_store: str):
        self._chunk_size = chunk_size
        self._cache_store = cache_store

    def deliver(self):
        pass
