from libs.config import parse_config
import libs.const as const
from libs.transmitter_preprocess import make_indexes, preproccess_no_cas_transmitter
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
from libs.delivery_systems.zsync import Zsync


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
    parser.add_argument("--optimal", action="store_true")

    parser.add_argument("--init-iter", type=int, default=5)
    parser.add_argument("--n-iter", type=int, default=25)
    return parser.parse_args()


def create_dirs(config):
    os.makedirs(config.result_plot_store, exist_ok=True)
    os.makedirs(config.result_data_store, exist_ok=True)
    os.makedirs(os.path.dirname(config.dest_path), exist_ok=True)


def check_need_for_preprocess(transmitter_name, versions):
    for version in versions:
        if f"{transmitter_name}_local" not in version.src_path:
            return False
    return True


def preprocess(config, chunk_sizes):
    for transmitter_name in config.cas_transmitters:
        transmitter_class = const.CAS_TRANSMITTERS[transmitter_name]
        make_indexes(
            transmitter_class,
            chunk_sizes=chunk_sizes[transmitter_name],
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
    for transmitter_name in config.other_transmitters:
        if check_need_for_preprocess(transmitter_name, config.versions):
            transmitter_class = const.OTHER_TRANSMITTERS[transmitter_name]
            preproccess_no_cas_transmitter(
                transmitter_class,
                sources_list=[
                    version.src_path[f"{transmitter_name}_local"]
                    for version in config.versions
                ],
            )


def calculate_cache_hit(config, chunk_sizes, verbose, create_average=True):
    average_cache_hits_by_transmitter = []
    for transmitter_name in config.cas_transmitters:
        cache_hits = calculate_cache_hit_by_indexes(
            chunk_sizes[transmitter_name],
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
            chunk_sizes[transmitter_name],
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
            chunk_sizes[transmitter_name],
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
    if create_average:
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


def deliver_experimentally(config, chunk_sizes, target, verbose):
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
            chunk_sizes=chunk_sizes[transmitter_name],
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


def find_optimal_chunk_size(config, target, args):
    chunk_sizes = dict()
    for transmitter_name in config.cas_transmitters:
        transmitter_class = const.CAS_TRANSMITTERS[transmitter_name]
        chunk_sizes[transmitter_name] = [
            optimize_chunk_size(
                transmitter_class,
                local_version_remote_store=os.path.join(
                    config.cas_config.local_version_of_remote_storage, transmitter_name
                ),
                remote_cache_store=os.path.join(
                    config.cas_config.remote_storage[transmitter_name], transmitter_name
                ),
                local_cache_store=os.path.join(
                    config.cas_config.local_cache_store, transmitter_name
                ),
                index_store=os.path.join(
                    config.cas_config.index_storage, transmitter_name
                ),
                versions=config.versions,
                target_function=get_target_function(
                    target, config.cas_transmitters[transmitter_name]
                ),
                dest_path=config.dest_path.format(transmitter_name),
                log_file=os.path.join(
                    join_dirs(config.result_data_store, transmitter_name),
                    "bayesian_optimization.log",
                ),
                init_point=args.init_iter,
                n_iter=args.n_iter,
            )
        ]
    return chunk_sizes


def main():
    args = parse_args()
    config = parse_config(args.config_file)
    create_dirs(config)
    if args.optimal:
        chunk_sizes = find_optimal_chunk_size(config, target=args.target, args=args)
    else:
        chunk_sizes = {
            key: config.cas_config.chunk_sizes for key in config.cas_transmitters
        }
    if not args.only_deliver:
        preprocess(config, chunk_sizes)
    if not args.only_chunking:
        calculate_cache_hit(
            config, chunk_sizes, args.verbose, create_average=not args.optimal
        )
        if not args.only_cache_hit:
            deliver_experimentally(config, chunk_sizes, args.target, args.verbose)


if __name__ == "__main__":
    main()
