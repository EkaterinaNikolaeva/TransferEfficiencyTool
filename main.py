from make_chunking.make_chunking import make_chunking
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="subcommand help")
    make_parser = subparsers.add_parser("make")
    make_parser.add_argument("source")
    make_parser.add_argument("-s", "--store", required=True)
    make_parser.add_argument("-m", "--chunk-size", default="16:64:256")
    make_parser.add_argument("--seed", required=True)
    make_parser.set_defaults(func=cmd_make)
    return parser.parse_args()


def cmd_make(args):
    make_chunking(args.store, args.seed, args.source, args.chunk_size)


def main():
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
