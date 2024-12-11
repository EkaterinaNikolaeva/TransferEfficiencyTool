import subprocess
import logging
from typing import List

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def run(command: str):
    logger.info(command)
    try:
        output = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        logger.error("Return code: {}".format(e.returncode))
        exit(e.returncode)
    logger.info("OK")
    return str(output)


def create_network_problems():
    clear()
    run("tc qdisc add dev lo root handle 1: htb default 12")

    run("tc class add dev lo parent 1: classid 1:1 htb rate 50mbit")

    run("tc qdisc add dev lo parent 1:1 handle 10: netem delay 100ms loss 1%")

    run("iptables -t mangle -A OUTPUT -p tcp --sport 8000 -j MARK --set-mark 1")
    run("iptables -t mangle -A OUTPUT -p tcp --sport 22 -j MARK --set-mark 1")

    run("tc filter add dev lo protocol ip handle 1 fw flowid 1:1")


def clear():
    run("tc qdisc del dev lo root || true")
    run(
        "sudo iptables -t mangle -D OUTPUT -p tcp --sport 22 -j MARK --set-mark 1 || true"
    )
    run(
        "sudo iptables -t mangle -D OUTPUT -p tcp --sport 8000 -j MARK --set-mark 1 || true"
    )


def main():
    create_network_problems()


if __name__ == "__main__":
    main()
