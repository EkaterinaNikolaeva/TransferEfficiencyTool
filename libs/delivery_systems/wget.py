from libs.delivery_systems.no_cas_transmitter import NoCasTransmitter
from util.exec import run


class Wget(NoCasTransmitter):
    def deliver(self, source, output):
        run(
            [
                "wget",
                source,
                "--output-file",
                output,
            ]
        )
