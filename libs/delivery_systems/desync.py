from libs.delivery_systems.empirical_cas_delivery import EmpiricalCasDelivery
from util.exec import run
from util.index_name import validate_index_name, IncorrectIndexFileName
import os
from typing import List
import logging


class Desync(EmpiricalCasDelivery):
    def _make_chunking_dir(self, source, index_store, chunk_size):
        run(
            [
                "desync",
                "tar",
                "-i",
                "-s",
                self._cache_store,
                "-m",
                chunk_size,
                index_store,
                source,
            ]
        )

    def make_chunking(self, source, index_store, chunk_size="16:64:256"):
        try:
            index_store = validate_index_name(index_store, source)
        except IncorrectIndexFileName as e:
            logging.error(
                "Exception when validating index store file name: {}".format(e.message)
            )
            exit(1)
        if os.path.isdir(source):
            self._make_chunking_dir(source, index_store, chunk_size)
            return
        run(
            [
                "desync",
                "make",
                "-m",
                chunk_size,
                "-s",
                self._cache_store,
                index_store,
                source,
            ]
        )

    def deliver(self, output, index_store):
        untar_index_flag = []
        command = "extract"
        if index_store.endswith(".caidx"):
            command = "untar"
            untar_index_flag = ["-i", "--no-same-owner"]
        run(
            [
                "desync",
                command,
                "-s",
                self._cache_store,
                "-c",
                self._local_cache_store,
                index_store,
                output,
            ]
            + untar_index_flag
        )
