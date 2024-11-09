from abc import ABC


class EmpiricalCasDelivery(ABC):
    def __init__(self, cache_store: str, local_cache_store: str):
        self._cache_store = cache_store
        self._local_cache_store = local_cache_store

    def make_chunking(self, source, index_store, chunk_size="16:64:256"):
        pass

    def deliver(self, output, index_store):
        pass
