from scapy.all import sniff
import signal
import sys
import argparse
import time


traffic_counter = 0
FACTOR = 1


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", required=True)
    parser.add_argument("-i", "--iface", required=True)
    return parser.parse_args()


def sigint_handler(sig, frame):
    global traffic_counter
    print(traffic_counter / FACTOR)
    sys.exit(0)


def monitor_traffic(packet):
    global traffic_counter
    traffic_counter += len(packet)


def main():
    global FACTOR
    args = parse_args()
    if args.iface == "lo":  # https://github.com/secdev/scapy/issues/1702
        FACTOR = 2  # https://stackoverflow.com/questions/52232080/scapy-sniff-the-packet-multiple-times
    signal.signal(signal.SIGINT, sigint_handler)
    sniff(filter="port {}".format(args.port), iface=args.iface, prn=monitor_traffic)


if __name__ == "__main__":
    main()
