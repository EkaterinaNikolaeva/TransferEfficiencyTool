from abc import ABC


class EmpiricalCasDelivery(ABC):
    def __init__(self, cache_store: str, index_store: str):
        self._cache_store = cache_store
        self._index_store = index_store

    def make_chunking(self, source, chunk_size="16:64:256"):
        pass

    def deliver(self, local_cache_store, output):
        pass
