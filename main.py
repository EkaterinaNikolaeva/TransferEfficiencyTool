from empirical_delivery.desync import Desync
from empirical_delivery.casync import Casync
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="subcommand help")
    desync_parser = subparsers.add_parser("desync")
    desync_parser.add_argument("command")
    desync_parser.add_argument("index")
    desync_parser.add_argument("source")
    desync_parser.add_argument("-s", "--store", required=True)
    desync_parser.add_argument("-c", "--cache")
    desync_parser.add_argument("-m", "--chunk-size", default="16:64:256")
    desync_parser.set_defaults(func=desync)

    casync_parser = subparsers.add_parser("casync")
    casync_parser.add_argument("command")
    casync_parser.add_argument("index")
    casync_parser.add_argument("source")
    casync_parser.add_argument("-s", "--store", required=True)
    casync_parser.add_argument("-c", "--cache")
    casync_parser.add_argument("-m", "--chunk-size", default="16384:65536:262144")
    casync_parser.set_defaults(func=casync)

    return parser.parse_args()


def desync(args):
    desync_tranfer = Desync(args.store, args.index)
    if args.command == "make":
        desync_tranfer.make_chunking(args.source, args.chunk_size)
    elif args.command == "extract":
        desync_tranfer.deliver(args.cache, args.source)


def casync(args):
    casync_tranfer = Casync(args.store, args.index)
    if args.command == "make":
        casync_tranfer.make_chunking(args.source, args.chunk_size)
    elif args.command == "extract":
        casync_tranfer.deliver(args.cache, args.source)


def main():
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
