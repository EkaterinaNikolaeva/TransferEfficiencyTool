from .empirical_delivery import EmpiricalDelivery
from util.exec import run
from util.index_name import validate_index_name, IncorrectIndexFileName
from typing import List
import logging


class Casync(EmpiricalDelivery):
    def __init__(self, cache_store: str, index_store: str):
        self._cache_store = cache_store
        self._index_store = index_store

    def make_chunking(
        self,
        source,
        chunk_size="16:64:256",
    ):
        try:
            self._index_store = validate_index_name(self._index_store, source)
        except IncorrectIndexFileName as e:
            logging.error(
                "Exception when validating index store file name: {}".format(e.message)
            )
            exit(1)
        run(
            [
                "casync",
                "make",
                self._index_store,
                source,
                "--chunk-size",
                chunk_size,
                "--store",
                self._cache_store,
            ]
        )

    def deliver(self):
        pass
