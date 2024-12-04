from libs.target_function.target import Target
import subprocess
import os
import signal

BYTES_IN_MBYTE = 1024 * 1024


class Traffic(Target):
    def __init__(self, port, iface):
        self._port = port
        self._iface = iface

    def start(self) -> None:
        self._process = subprocess.Popen(
            [
                "sudo",
                "./traffic/traffic_counter_util.py",
                "--port",
                str(self._port),
                "-i",
                self._iface,
            ],  # TODO replace it with a deb package!!!
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            preexec_fn=os.setsid,
        )

    def finish(self) -> float:
        os.killpg(os.getpgid(self._process.pid), signal.SIGINT)
        self._process.wait()
        return float(self._process.stdout.readline()) / BYTES_IN_MBYTE
