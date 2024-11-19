from empirical_delivery.casync import Casync
from empirical_delivery.desync import Desync
from empirical_delivery.rsync import Rsync
from empirical_delivery.empirical_cas_delivery import EmpiricalCasDelivery

from util.index_name import validate_index_name
from util.plot import make_plot

import yaml
import time
import os.path
from dataclasses import dataclass

DESYNC = "desync"
CASYNC = "casync"
RSYNC = "rsync"


def preprocess():
    pass


def get_index_name():
    pass


def parse_config_file(config_file):
    with open(config_file) as f:
        config = yaml.safe_load(f)
    return config


def safe_data_to_file(file_name, data):
    with open(file_name, "w") as f:
        yaml.dump(data, f)


def deliver(transmitter: EmpiricalCasDelivery, path_index_file: str, destination: str):
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
    dest_path: str,
    only_make_chunking=False,
    only_deliver=False,
):
    y_data = []
    for version in versions:
        index_file_name = validate_index_name(version["name"], version["src_path"])
        path_index_file = os.path.join(index_storage_name, index_file_name)
        if not only_deliver:
            transmitter.make_chunking(version["src_path"], path_index_file)
        if not only_make_chunking:
            start = time.time()
            transmitter.deliver(dest_path, path_index_file)
            end = time.time()
            y_data.append(end - start)
    return y_data


def transfer_using_rsync(transmitter, versions, dest_path, only_make_chunking):
    if only_make_chunking:
        return
    y_data = []
    for version in versions:
        start = time.time()
        transmitter.deliver(version["rsync_src_path"], dest_path)
        end = time.time()
        y_data.append(end - start)
    return y_data


def run(config_file, only_make_chunking=False, only_deliver=False):
    config = parse_config_file(config_file)
    version_names = [version["name"] for version in config["versions"]]
    plot_data = {}

    desync_transmitter = Desync(
        config.get("remote_storage_desync") or config["remote_storage"],
        join_dirs(config["local_cache_store"], DESYNC),
    )
    plot_data[DESYNC] = transfer_using_cas(
        desync_transmitter,
        config["versions"],
        join_dirs(config["index_storage"], DESYNC),
        config["dest_path"].format(DESYNC),
        only_make_chunking,
        only_deliver,
    )

    casync_transmitter = Casync(
        config.get("remote_storage_casync") or config["remote_storage"],
        join_dirs(config["local_cache_store"], CASYNC),
        config["local_storage_for_casync_make"],
    )
    plot_data[CASYNC] = transfer_using_cas(
        casync_transmitter,
        config["versions"],
        join_dirs(config["index_storage"], CASYNC),
        config["dest_path"].format(CASYNC),
        only_make_chunking,
        only_deliver,
    )

    rsync_transmitter = Rsync()
    plot_data[RSYNC] = transfer_using_rsync(
        rsync_transmitter,
        config["versions"],
        config["dest_path"].format(RSYNC),
        only_make_chunking,
    )

    if not only_make_chunking:
        safe_data_to_file(config["result_data_file"], plot_data)
        make_plot(config["name"], version_names, plot_data, config["result_plot_file"])
