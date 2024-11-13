from empirical_delivery.casync import Casync
from empirical_delivery.desync import Desync
from empirical_delivery.rsync import Rsync
from empirical_delivery.empirical_cas_delivery import EmpiricalCasDelivery

from util.index_name import validate_index_name
from util.plot import make_plot

import yaml
import time
import os.path

DESYNC = "desync"
CASYNC = "casync"


def preprocess():
    pass


def get_index_name():
    pass


def parse_config_file(config_file):
    with open(config_file) as f:
        config = yaml.safe_load(f)
    return config


def deliver(transmitter, path_index_file, destination):
    start = time.time()
    transmitter.deliver(destination, path_index_file)
    end = time.time()
    return end - start


def make_chunking(transmitter, path_index_file, source):
    transmitter.make_chunking(source, path_index_file)


def join_dirs(prefix, suffix):
    name = os.path.join(prefix, suffix)
    os.makedirs(name, exist_ok=True)
    return name


def transfer_using_cas(
    transmitter: EmpiricalCasDelivery,
    versions,
    index_storage_name: str,
    only_make_chunking=False,
    only_deliver=False,
):
    y_data = []
    for version in versions:
        index_file_name = validate_index_name(version[0], version[1])
        path_index_file = os.path.join(index_storage_name, index_file_name)
        print(path_index_file, index_storage_name, index_file_name)
        if not only_deliver:
            transmitter.make_chunking(version[1], path_index_file)
        if not only_make_chunking:
            start = time.time()
            transmitter.deliver(version[2], path_index_file)
            end = time.time()
            y_data.append(end - start)
    return y_data


def run(config_file, only_make_chunking=False, only_deliver=False):
    config = parse_config_file(config_file)
    version_names = [version[0] for version in config["versions"]]
    plot_data = {}

    casync_transmitter = Casync(
        config["remote_storage"],
        join_dirs(config["local_cache_store"], CASYNC),
        config["local_storage_for_casync_make"],
    )
    plot_data[CASYNC] = transfer_using_cas(
        casync_transmitter,
        config["versions"],
        join_dirs(config["index_storage"], CASYNC),
        only_make_chunking,
        only_deliver,
    )
    desync_transmitter = Desync(
        config["remote_storage"], join_dirs(config["local_cache_store"], DESYNC)
    )
    plot_data[DESYNC] = transfer_using_cas(
        desync_transmitter,
        config["versions"],
        join_dirs(config["index_storage"], DESYNC),
        only_make_chunking,
        only_deliver,
    )

    if not only_make_chunking:
        make_plot(config["name"], version_names, plot_data)
