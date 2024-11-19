from delivery_systems.desync import Desync
from delivery_systems.casync import Casync
from delivery_systems.rsync import Rsync
import empirical_delivery.experiment as experiment
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="subcommand help")

    experiment_parser = subparsers.add_parser("experiment")
    experiment_parser.add_argument("--config-file", required=True)
    experiment_parser.add_argument("--only-chunking", action="store_true")
    experiment_parser.add_argument("--only-deliver", action="store_true")
    experiment_parser.set_defaults(func=run_experiment)

    desync_parser = subparsers.add_parser("desync")
    desync_parser.add_argument("command")
    desync_parser.add_argument("index")
    desync_parser.add_argument("source")
    desync_parser.add_argument("-s", "--store", required=True)
    desync_parser.add_argument("-c", "--cache", default=None)
    desync_parser.add_argument("-m", "--chunk-size", default="16:64:256")
    desync_parser.set_defaults(func=desync)

    casync_parser = subparsers.add_parser("casync")
    casync_parser.add_argument("command")
    casync_parser.add_argument("index")
    casync_parser.add_argument("source")
    casync_parser.add_argument("-s", "--store", required=True)
    casync_parser.add_argument("-c", "--cache", default=None)
    casync_parser.add_argument("-m", "--chunk-size", default="16384:65536:262144")
    casync_parser.set_defaults(func=casync)

    rsync_parser = subparsers.add_parser("rsync")
    rsync_parser.add_argument("source")
    rsync_parser.add_argument("output")
    rsync_parser.set_defaults(func=rsync)

    return parser.parse_args()


def run_experiment(args):
    experiment.run(args.config_file, args.only_chunking, args.only_deliver)


def desync(args):
    desync_tranfer = Desync(args.store, args.cache)
    if args.command == "make":
        desync_tranfer.make_chunking(args.source, args.index, args.chunk_size)
    elif args.command == "extract":
        desync_tranfer.deliver(args.source, args.index)


def casync(args):
    casync_tranfer = Casync(args.store, args.cache)
    if args.command == "make":
        casync_tranfer.make_chunking(args.source, args.index, args.chunk_size)
    elif args.command == "extract":
        casync_tranfer.deliver(args.source, args.index)


def rsync(args):
    rsync_tranfer = Rsync()
    rsync_tranfer.deliver(args.source, args.output)


def main():
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
