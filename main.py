from libs.config import parse_config
import libs.const as const
from libs.make_indexes import make_indexes
from libs.cache_hit import (
    calculate_cache_hit_by_indexes,
    calculate_average_cache_hit,
    calculate_importance_last_version_by_indexes,
)
from libs.empirical_delivery import (
    transfer_using_cas_all_chunks,
    transfer_without_cache,
)
from util.join_dirs import join_dirs
from util.plot import make_plot, Subplot
from util.dump_data import safe_data_to_file
import argparse
import os
import libs.target_function as target_functions
from libs.optimization import optimize_chunk_size


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config-file", required=True)
    parser.add_argument(
        "--target", choices=[const.TRAFFIC, const.TIME], default=const.TIME
    )
    parser.add_argument("--only-chunking", action="store_true")
    parser.add_argument("--only-deliver", action="store_true")
    parser.add_argument("--only-cache-hit", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")

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


def calculate_cache_hit(config, verbose):
    average_cache_hits_by_transmitter = []
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
        average_cache_hits_by_transmitter.append(
            Subplot(name=transmitter_name, data=average_cache_hits)
        )
        calculate_importance_last_version_by_indexes(
            os.path.join(config.cas_config.index_storage, transmitter_name),
            config.versions,
            data_file=os.path.join(
                join_dirs(config.result_data_store, transmitter_name),
                "importance_latest_version.yaml",
            ),
            plot_file=os.path.join(
                join_dirs(config.result_data_store, transmitter_name),
                "importance_latest_version.png",
            ),
        )
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
        verbose=verbose,
    )
    safe_data_to_file(
        os.path.join(
            config.result_data_store,
            "average_cache_hit.yaml",
        ),
        data=average_cache_hits_by_transmitter,
    )


def save_data(config, data, filename, middle=False):
    if middle:
        filename = "tmp_{}".format(filename)
    safe_data_to_file(
        os.path.join(
            config.result_data_store,
            filename,
        ),
        data=data,
    )


def get_target_function(target, transmitter_params):
    if target == const.TIME:
        return target_functions.time.Time()
    elif target == const.TRAFFIC:
        return target_functions.traffic.Traffic(transmitter_params.port, "lo")


def deliver_experimentally(config, target, verbose):
    plot_data = []
    for transmitter_name in config.cas_transmitters:
        os.makedirs(
            os.path.dirname(config.dest_path.format(transmitter_name)), exist_ok=True
        )
        transmitter_class = const.CAS_TRANSMITTERS[transmitter_name]
        plot_data += transfer_using_cas_all_chunks(
            transmitter_name=transmitter_name,
            transmitter_class=transmitter_class,
            target_function=get_target_function(
                target, config.cas_transmitters[transmitter_name]
            ),
            chunk_sizes=config.cas_config.chunk_sizes,
            remote_store=os.path.join(
                config.cas_config.remote_storage[transmitter_name], transmitter_name
            ),
            local_cache_dir=os.path.join(
                config.cas_config.local_cache_store, transmitter_name
            ),
            index_store=os.path.join(config.cas_config.index_storage, transmitter_name),
            versions=config.versions,
            dest_path=config.dest_path.format(transmitter_name),
        )
        save_data(config, plot_data, "time_comparison.yaml", middle=True)
    for transmitter_name in config.other_transmitters:
        transmitter_class = const.OTHER_TRANSMITTERS[transmitter_name]
        plot_data += transfer_without_cache(
            transmitter_name=transmitter_name,
            transmitter_class=transmitter_class,
            target_function=get_target_function(
                target, config.other_transmitters[transmitter_name]
            ),
            versions=config.versions,
            dest_path=config.dest_path.format(transmitter_name),
        )
    make_plot(
        "{} comparison of different transmitters".format(target),
        [version.name for version in config.versions],
        plot_data,
        plot_file=os.path.join(
            config.result_plot_store, "{}_comparison.png".format(target)
        ),
        xlabel="Version",
        ylabel=target,
        verbose=verbose,
    )
    save_data(config, plot_data, "{}_comparison.yaml".format(target))


def find_optimal_chunk_size(config, target):
    optimize_chunk_size(
        local_src_path=os.path.join(
            config.cas_config.local_version_of_remote_storage, "desync"
        ),
        remote_cache_store=os.path.join(
            config.cas_config.remote_storage["desync"], "desync"
        ),
        local_cache_store=os.path.join(config.cas_config.local_cache_store, "desync"),
        index_store=os.path.join(config.cas_config.index_storage, "desync"),
        versions=config.versions,
        target_function=get_target_function(target, config.cas_transmitters["desync"]),
        dest_path=config.dest_path.format("desync"),
    )


def main():
    args = parse_args()
    config = parse_config(args.config_file)
    find_optimal_chunk_size(config, target=args.target)
    # if not args.only_deliver:
    #     preprocess(config)
    # if not args.only_chunking:
    #     calculate_cache_hit(config, args.verbose)
    #     if not args.only_cache_hit:
    #         deliver_experimentally(config, args.target, args.verbose)


if __name__ == "__main__":
    main()
