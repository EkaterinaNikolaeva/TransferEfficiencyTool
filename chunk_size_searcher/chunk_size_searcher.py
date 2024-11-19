from delivery_systems.desync import Desync

from util.join_dirs import join_dirs

import os

CHUNK_SIZES_IN_KB = [8, 16, 32, 64, 96, 128, 192, 256, 384, 512]


def make_indexes(
    transmitter_class,
    remote_store,
    local_cache_dir,
    index_store,
    version_list,
    factor=1,
):
    for chunk_size in CHUNK_SIZES_IN_KB:
        transmitter = transmitter_class(
            join_dirs(remote_store, str(chunk_size)),
            join_dirs(local_cache_dir, str(chunk_size)),
        )
        avg_chunk_size_for_transmitter = chunk_size * factor
        for version in version_list:
            transmitter.make_chunking(
                version,
                os.path.join(
                    join_dirs(index_store, str(chunk_size)), os.path.basename(version)
                ),
                "{}:{}:{}".format(
                    avg_chunk_size_for_transmitter // 4,
                    avg_chunk_size_for_transmitter,
                    avg_chunk_size_for_transmitter * 4,
                ),
            )
