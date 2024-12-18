from network_conditions import NetworkConditions
import subprocess
import logging
from typing import List
import argparse


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


def create_network_problems(network_conditions):
    clear(network_conditions)
    run("sudo tc qdisc add dev lo root handle 1: htb default 12")
    run(
        "sudo tc class add dev lo parent 1: classid 1:1 htb rate {}mbit".format(
            network_conditions.bandwidth
        )
    )
    run(
        "sudo tc qdisc add dev lo parent 1:1 handle 10: netem delay {}ms loss {}%".format(
            network_conditions.delay, network_conditions.loss
        )
    )
    for port in network_conditions.ports:
        run(
            "sudo iptables -t mangle -A OUTPUT -p tcp --sport {} -j MARK --set-mark 1".format(
                port
            )
        )
        run(
            "sudo iptables -t mangle -A OUTPUT -p tcp --dport {} -j MARK --set-mark 1".format(
                port
            )
        )
    run("sudo tc filter add dev lo protocol ip handle 1 fw flowid 1:1")


def clear(network_conditions):
    run("sudo tc qdisc del dev lo root || true")
    for port in network_conditions.ports:
        run(
            "sudo iptables -t mangle -D OUTPUT -p tcp --sport {} -j MARK --set-mark 1 || true".format(
                port
            )
        )
        run(
            "sudo iptables -t mangle -D OUTPUT -p tcp --dport {} -j MARK --set-mark 1 || true".format(
                port
            )
        )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clear", action="store_true")
    parser.add_argument("--delay", type=int, default=40)
    parser.add_argument("--delay-delta", type=int, default=10)
    parser.add_argument("--bandwidth", type=int, default=100)
    parser.add_argument("--distribution-type", type=str, default="normal")
    parser.add_argument("--loss", type=float, default=0.5)
    parser.add_argument("--port", nargs="+", type=int)
    return parser.parse_args()


def main():
    args = parse_args()
    print(args.port)
    network_conditions = NetworkConditions(
        delay=args.delay,
        delay_delta=args.delay_delta,
        distribution_type=args.distribution_type,
        loss=args.loss,
        bandwidth=args.bandwidth,
        ports=args.port,
    )
    if args.clear:
        clear(network_conditions)
        return
    create_network_problems(network_conditions)


if __name__ == "__main__":
    main()
