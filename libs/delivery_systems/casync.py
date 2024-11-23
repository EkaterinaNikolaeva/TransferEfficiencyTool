from libs.delivery_systems.empirical_cas_delivery import EmpiricalCasDelivery
from util.exec import run
from util.index_name import validate_index_name, IncorrectIndexFileName
from typing import List
import logging


class Casync(EmpiricalCasDelivery):
    def __init__(self, cache_store: str, local_cache_store: str):
        super().__init__(cache_store, local_cache_store)

    def make_chunking(
        self,
        source,
        index_store,
        chunk_size="16384:65536:262144",
    ):
        try:
            index_store = validate_index_name(index_store, source)
        except IncorrectIndexFileName as e:
            logging.error(
                "Exception when validating index store file name: {}".format(e.message)
            )
            exit(1)
        run(
            [
                "casync",
                "make",
                index_store,
                source,
                "--chunk-size",
                chunk_size,
                "--store",
                self._cache_store,
            ]
        )

    def deliver(self, output, index_store):
        print(self._local_cache_store)
        run(
            [
                "casync",
                "extract",
                index_store,
                output,
                "--store",
                self._cache_store,
                "--cache",
                self._local_cache_store,
                "--reflink",
                "no",
            ]
        )
