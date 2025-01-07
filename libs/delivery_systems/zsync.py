from libs.delivery_systems.no_cas_transmitter import NoCasTransmitter
from util.exec import run


class Zsync(NoCasTransmitter):
    def preprocess(self, src_file):
        run(["zsyncmake", "-z", src_file, "-o", f"{src_file}.zsync"])

    def deliver(self, zsync_source, output):
        run(
            [
                "zsync",
                zsync_source,
                "-o",
                output,
            ]
        )
