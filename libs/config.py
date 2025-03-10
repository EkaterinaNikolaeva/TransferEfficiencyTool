from dataclasses import dataclass
from typing import List, Dict
import yaml
from dacite import from_dict


@dataclass(frozen=True)
class Version:
    name: str
    src_path: Dict[str, str]


@dataclass(frozen=True)
class TransmitterParams:
    port: int


@dataclass(frozen=True)
class CasDeliverConfig:
    local_cache_store: str
    index_storage: str
    local_version_of_remote_storage: str
    chunk_sizes: List[int]
    remote_storage: Dict[str, str]


@dataclass(frozen=True)
class Config:
    name: str
    cas_config: CasDeliverConfig
    versions: List[Version]
    cas_transmitters: Dict[str, TransmitterParams]
    other_transmitters: Dict[str, TransmitterParams]
    dest_path: str
    result_data_store: str
    result_plot_store: str


def parse_config(config_file):
    with open(config_file) as f:
        config_data = yaml.safe_load(f)
    config = from_dict(Config, config_data)
    return config
