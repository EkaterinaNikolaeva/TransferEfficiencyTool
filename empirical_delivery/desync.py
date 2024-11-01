from .empirical_delivery import EmpiricalDelivery
from util.exec import run
from util.index_name import validate_index_name, IncorrectIndexFileName
import os
from typing import List
import logging


class Desync(EmpiricalDelivery):
    def __init__(self, cache_store: str, index_store: str):
        self._cache_store = cache_store
        self._index_store = index_store

    def _make_chunking_dir(self, source, chunk_size):
        run(
            [
                "desync",
                "tar",
                "-i",
                "-s",
                self._cache_store,
                "-m",
                chunk_size,
                self._index_store,
                source,
            ]
        )

    def make_chunking(self, source, chunk_size="16:64:256"):
        try:
            self._index_store = validate_index_name(self._index_store, source)
        except IncorrectIndexFileName as e:
            logging.error(
                "Exception when validating index store file name: {}".format(e.message)
            )
            exit(1)
        if os.path.isdir(source):
            self._make_chunking_dir(source, chunk_size)
            return
        run(
            [
                "desync",
                "make",
                "-m",
                chunk_size,
                "-s",
                self._cache_store,
                self._index_store,
                source,
            ]
        )

    def deliver(self):
        pass
