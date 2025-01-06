from util.index_name import validate_index_name
from util.plot import Subplot
from util.join_dirs import join_dirs

import os.path


def transfer_using_cas(transmitter, target_function, index_dir, dest_path, versions):
    y_data = []
    for version in versions:
        index_file_name = validate_index_name(version.name, version.src_path["local"])
        path_index_file = os.path.join(index_dir, index_file_name)
        target_function.start()
        transmitter.deliver(dest_path, path_index_file)
        y_data.append(target_function.finish())
    return y_data


def transfer_using_cas_for_chunk_size(
    chunk_size,
    transmitter_class,
    remote_store,
    local_cache_dir,
    index_store,
    target_function,
    dest_path,
    versions,
):
    transmitter = transmitter_class(
        join_dirs(remote_store, str(chunk_size)),
        join_dirs(local_cache_dir, str(chunk_size)),
    )
    index_dir = join_dirs(index_store, str(chunk_size))
    return transfer_using_cas(
        transmitter=transmitter,
        target_function=target_function,
        index_dir=index_dir,
        dest_path=dest_path,
        versions=versions,
    )


def transfer_using_cas_all_chunks(
    transmitter_name,
    transmitter_class,
    target_function,
    chunk_sizes,
    remote_store,
    local_cache_dir,
    index_store,
    versions,
    dest_path: str,
):
    results = []
    for chunk_size in chunk_sizes:
        y_data = transfer_using_cas_for_chunk_size(
            chunk_size,
            transmitter_class,
            remote_store,
            local_cache_dir,
            index_store,
            target_function,
            dest_path,
            versions,
        )
        results.append(Subplot(name=f"{transmitter_name}-{chunk_size}", data=y_data))
    return results


def transfer_without_cache(
    transmitter_name, transmitter_class, target_function, versions, dest_path
):
    transmitter = transmitter_class()
    y_data = []
    for version in versions:
        target_function.start()
        transmitter.deliver(version.src_path[transmitter_name], dest_path)
        y_data.append(target_function.finish())
    return [Subplot(transmitter_name, y_data)]
