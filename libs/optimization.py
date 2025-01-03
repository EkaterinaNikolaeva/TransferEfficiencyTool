from bayes_opt import BayesianOptimization
from libs.delivery_systems.desync import Desync
from libs.make_indexes import make_indexes_for_chunk_size
from libs.empirical_delivery import transfer_using_cas_for_chunk_size
import os
import shutil


def try_chunk_size(
    chunk_size,
    local_src_path,
    remote_cache_store,
    local_cache_store,
    index_store,
    versions,
    target_function,
    dest_path,
):
    chunk_size = int(chunk_size)
    for file_name in os.listdir(local_cache_store):
        file_path = os.path.join(local_cache_store, file_name)
        shutil.rmtree(file_path)
    make_indexes_for_chunk_size(
        chunk_size, Desync, local_src_path, local_cache_store, index_store, versions
    )
    y_data = transfer_using_cas_for_chunk_size(
        chunk_size,
        Desync,
        remote_cache_store,
        local_cache_store,
        index_store,
        target_function,
        dest_path,
        versions,
    )
    return -sum(y_data) / len(y_data)


def optimize_chunk_size(
    local_src_path,
    remote_cache_store,
    local_cache_store,
    index_store,
    versions,
    target_function,
    dest_path,
):
    pbounds = {"chunk_size": (8, 20000)}
    optimizer = BayesianOptimization(
        f=lambda chunk_size: try_chunk_size(
            chunk_size,
            local_src_path,
            remote_cache_store,
            local_cache_store,
            index_store,
            versions,
            target_function,
            dest_path,
        ),
        pbounds=pbounds,
        random_state=1,
    )
    optimizer.maximize(
        init_points=5,
        n_iter=25,
    )
    print(optimizer.max)
