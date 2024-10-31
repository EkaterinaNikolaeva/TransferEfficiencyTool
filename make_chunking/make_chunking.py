import subprocess
import logging
from util.exec import run


def make_chunking(chunk_store, caibx_store, source, chunk_size=64):
    run(
        [
            "desync",
            "make",
            "-m",
            chunk_size,
            "-s",
            chunk_store,
            caibx_store,
            source,
        ]
    )
