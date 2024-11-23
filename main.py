from libs.config import parse_config
import libs.const as const
from libs.make_indexes import make_indexes
from libs.cache_hit import calculate_cache_hit_by_indexes, calculate_average_cache_hit
from util.join_dirs import join_dirs
from util.plot import make_plot
from util.dump_data import safe_data_to_file
import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config-file", required=True)
    parser.add_argument("--only-chunking", action="store_true")
    parser.add_argument("--only-deliver", action="store_true")

    return parser.parse_args()


def preprocess(config):
    for transmitter_name in config.cas_transmitters:
        transmitter_class = const.CAS_TRANSMITTERS[transmitter_name]
        make_indexes(
            transmitter_class,
            chunk_sizes=config.cas_config.chunk_sizes,
            remote_store=os.path.join(
                config.cas_config.local_version_of_remote_storage, transmitter_name
            ),
            local_cache_dir=os.path.join(
                config.cas_config.local_cache_store, transmitter_name
            ),
            index_store=os.path.join(config.cas_config.index_storage, transmitter_name),
            version_list=config.versions,
            factor=const.CAS_CHUNK_SIZES_FACTOR[transmitter_name],
        )


def calculate_cache_hit(config):
    average_cache_hits_by_transmitter = {}
    for transmitter_name in config.cas_transmitters:
        cache_hits = calculate_cache_hit_by_indexes(
            os.path.join(config.cas_config.index_storage, transmitter_name),
            config.versions,
            data_file=os.path.join(
                join_dirs(config.result_data_store, transmitter_name), "cache_hit.yaml"
            ),
            plot_file=os.path.join(
                join_dirs(config.result_plot_store, transmitter_name), "cache_hit.png"
            ),
        )
        average_cache_hits = calculate_average_cache_hit(
            cache_hits,
            config.cas_config.chunk_sizes,
            data_file=os.path.join(
                join_dirs(config.result_data_store, transmitter_name),
                "average_cache_hit.yaml",
            ),
            plot_file=os.path.join(
                join_dirs(config.result_plot_store, transmitter_name),
                "average_cache_hit.png",
            ),
        )
        average_cache_hits_by_transmitter[transmitter_name] = average_cache_hits
    print(average_cache_hits_by_transmitter)
    make_plot(
        "Average cache hit",
        config.cas_config.chunk_sizes,
        average_cache_hits_by_transmitter,
        os.path.join(
            config.result_plot_store,
            "average_cache_hit.png",
        ),
        xlabel="Chunk sizes",
        ylabel="Cache hit",
    )
    safe_data_to_file(
        os.path.join(
            config.result_data_store,
            "average_cache_hit.yaml",
        ),
        data=average_cache_hits_by_transmitter,
    )


def main():
    args = parse_args()
    config = parse_config(args.config_file)
    if not args.only_deliver:
        preprocess(config)
    calculate_cache_hit(config)


if __name__ == "__main__":
    main()
