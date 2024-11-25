from util.index_name import validate_index_name
from util.plot import Subplot
from util.join_dirs import join_dirs

import time
import os.path


def transfer_using_cas(
    transmitter_name,
    transmitter_class,
    chunk_sizes,
    remote_store,
    local_cache_dir,
    index_store,
    versions,
    dest_path: str,
):
    results = []
    for chunk_size in chunk_sizes:
        transmitter = transmitter_class(
            join_dirs(remote_store, str(chunk_size)),
            join_dirs(local_cache_dir, str(chunk_size)),
        )
        y_data = []
        index_dir = join_dirs(index_store, str(chunk_size))
        for version in versions:
            index_file_name = validate_index_name(version.name, version.src_path)
            path_index_file = os.path.join(index_dir, index_file_name)
            start = time.time()
            transmitter.deliver(dest_path, path_index_file)
            end = time.time()
            y_data.append(end - start)
        results.append(Subplot(name=f"{transmitter_name}-{chunk_size}", data=y_data))
    return results


def transfer_using_rsync(transmitter_name, transmitter_class, versions, dest_path):
    transmitter = transmitter_class()
    y_data = []
    for version in versions:
        start = time.time()
        transmitter.deliver(version.rsync_src_path, dest_path)
        end = time.time()
        y_data.append(end - start)
    return [Subplot(transmitter_name, y_data)]
