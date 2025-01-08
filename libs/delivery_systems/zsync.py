from libs.delivery_systems.no_cas_transmitter import NoCasTransmitter
from util.exec import run
import os


class Zsync(NoCasTransmitter):
    def preprocess(self, src_file):
        run(
            ["zsyncmake", os.path.basename(src_file), "-z"],
            cwd=os.path.dirname(src_file),
        )

    def deliver(self, zsync_source, output):
        run(
            [
                "zsync",
                zsync_source,
                "-o",
                output,
            ]
        )
