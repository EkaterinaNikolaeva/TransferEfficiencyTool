from empirical_delivery.casync import Casync
from empirical_delivery.desync import Desync
from empirical_delivery.rsync import Rsync

from util.index_name import validate_index_name
import yaml
import time
import os.path


def preprocess():
    pass


def get_index_name():
    pass


def parse_config_file(config_file):
    with open(config_file) as f:
        config = yaml.safe_load(f)
    return config


def desync(config):
    desync_transfer = Desync(config["remote_storage"], config["local_cache_store"])
    data = []
    for version in config["versions"]:
        index_file_name = validate_index_name(version[0], version[1])
        path_index_file = os.path.join(config["index_storage"], index_file_name)
        desync_transfer.make_chunking(version[1], path_index_file)
        start = time.time()
        desync_transfer.deliver(version[2], path_index_file)
        end = time.time()
        print(version[0], end - start)


def run(config_file):
    config = parse_config_file(config_file)
    desync(config)
