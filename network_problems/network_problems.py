from network_conditions import NetworkConditions
from real_network_conditions import REAL_CONDITIONS
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
    clear(network_conditions.ports)
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


def clear(ports):
    run("sudo tc qdisc del dev lo root || true")
    for port in ports:
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


def get_default_conditions(args):
    return REAL_CONDITIONS[args.conditions]


def get_customizable_conditions(args):
    return NetworkConditions(
        delay=args.delay,
        delay_delta=args.delay_delta,
        distribution_type=args.distribution_type,
        loss=args.loss,
        bandwidth=args.bandwidth,
    )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", nargs="+", type=int)

    action = parser.add_mutually_exclusive_group()
    action.add_argument("--clear", action="store_true")
    action.add_argument("--make", action="store_true")

    subparsers = parser.add_subparsers(dest="method")

    parser_default_conditions = subparsers.add_parser("default")
    parser_default_conditions.add_argument("conditions", choices=REAL_CONDITIONS.keys())

    parser_customizable_conditions = subparsers.add_parser("configure")
    parser_customizable_conditions.add_argument("--delay", type=int, default=40)
    parser_customizable_conditions.add_argument("--delay-delta", type=int, default=10)
    parser_customizable_conditions.add_argument("--bandwidth", type=int, default=100)
    parser_customizable_conditions.add_argument(
        "--distribution-type", type=str, default="normal"
    )
    parser_customizable_conditions.add_argument("--loss", type=float, default=0.5)

    return parser.parse_args()


def main():
    args = parse_args()
    if args.clear:
        clear(args.port)
        return
    if args.method == "default":
        network_conditions = REAL_CONDITIONS[args.conditions]
        network_conditions.ports = args.port
    else:
        network_conditions = NetworkConditions(
            delay=args.delay,
            delay_delta=args.delay_delta,
            distribution_type=args.distribution_type,
            loss=args.loss,
            bandwidth=args.bandwidth,
            ports=args.port,
        )
    print(network_conditions)
    create_network_problems(network_conditions)


if __name__ == "__main__":
    main()
