from util.exec import run
from util.index_name import validate_index_name, IncorrectIndexFileName
from typing import List
import os


class Wget:
    def deliver(self, source, output):
        run(
            [
                "wget",
                source,
                "--output-file",
                output,
            ]
        )
