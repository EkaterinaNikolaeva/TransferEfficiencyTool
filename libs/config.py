from dataclasses import dataclass
from typing import List
import yaml
from dacite import from_dict


@dataclass(frozen=True)
class Version:
    name: str
    src_path: str
    rsync_src_path: str


@dataclass(frozen=True)
class CasDeliverConfig:
    local_cache_store: str
    index_storage: str
    local_version_of_remote_storage: str
    chunk_sizes: List[int]
    remote_storage: str | None = None
    remote_storage_casync: str | None = None
    remote_storage_desync: str | None = None


@dataclass(frozen=True)
class Config:
    name: str
    cas_config: CasDeliverConfig
    versions: List[Version]
    cas_transmitters: List[str]
    rsync_transmitters: List[str]
    dest_path: str
    result_data_store: str
    result_plot_store: str


def parse_config(config_file):
    with open(config_file) as f:
        config_data = yaml.safe_load(f)
    config = from_dict(Config, config_data)
    return config
