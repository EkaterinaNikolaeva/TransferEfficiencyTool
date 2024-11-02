from util.exec import run
from util.index_name import validate_index_name, IncorrectIndexFileName
from typing import List
import os


class Rsync:
    def deliver(self, source, output):
        dir_flag = []
        if os.path.isdir(source):
            dir_flag = ["-r"]
        run(
            [
                "rsync",
                source,
                output,
            ]
            + dir_flag
        )
