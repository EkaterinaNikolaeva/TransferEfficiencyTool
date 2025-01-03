from libs.delivery_systems.desync import Desync

from util.join_dirs import join_dirs

import os


def make_indexes_for_chunk_size(
    chunk_size,
    transmitter_class,
    remote_store,
    local_cache_dir,
    index_store,
    version_list,
    factor=1,
):
    transmitter = transmitter_class(
        join_dirs(remote_store, str(chunk_size)),
        join_dirs(local_cache_dir, str(chunk_size)),
    )
    avg_chunk_size_for_transmitter = chunk_size * factor
    index_dir = join_dirs(index_store, str(chunk_size))
    for version in version_list:
        transmitter.make_chunking(
            version.src_path["local"],
            os.path.join(index_dir, os.path.basename(version.name)),
            "{}:{}:{}".format(
                avg_chunk_size_for_transmitter // 4,
                avg_chunk_size_for_transmitter,
                avg_chunk_size_for_transmitter * 4,
            ),
        )


def make_indexes(
    transmitter_class,
    chunk_sizes,
    remote_store,
    local_cache_dir,
    index_store,
    version_list,
    factor=1,
):
    for chunk_size in chunk_sizes:
        make_indexes_for_chunk_size(
            chunk_size,
            transmitter_class,
            remote_store,
            local_cache_dir,
            index_store,
            version_list,
            factor,
        )
