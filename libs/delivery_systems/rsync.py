from libs.delivery_systems.no_cas_transmitter import NoCasTransmitter
from util.exec import run
import os


class Rsync(NoCasTransmitter):
    def deliver(self, source, output):
        dir_flag = []
        if os.path.isdir(source):
            dir_flag = ["-r"]
        run(
            [
                "rsync",
                "-az",
                source,
                output,
            ]
            + dir_flag
        )
