from bayes_opt import BayesianOptimization
from bayes_opt.logger import JSONLogger, ScreenLogger
from bayes_opt.event import Events
from libs.make_indexes import make_indexes_for_chunk_size
from libs.empirical_delivery import transfer_using_cas_for_chunk_size
import os
import shutil


def try_chunk_size(
    chunk_size,
    transmitter_class,
    local_version_remote_store,
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
        chunk_size,
        transmitter_class,
        local_version_remote_store,
        local_cache_store,
        index_store,
        versions,
    )
    y_data = transfer_using_cas_for_chunk_size(
        chunk_size,
        transmitter_class,
        remote_cache_store,
        local_cache_store,
        index_store,
        target_function,
        dest_path,
        versions,
    )
    shutil.rmtree(os.path.join(local_version_remote_store, str(chunk_size)))
    shutil.rmtree(os.path.join(local_cache_store, str(chunk_size)))
    return -sum(y_data) / len(y_data)


def optimize_chunk_size(
    transmitter_class,
    local_version_remote_store,
    remote_cache_store,
    local_cache_store,
    index_store,
    versions,
    target_function,
    dest_path,
    log_file=None,
    init_point=5,
    n_iter=25,
):
    pbounds = {"chunk_size": (8, 20000)}
    optimizer = BayesianOptimization(
        f=lambda chunk_size: try_chunk_size(
            chunk_size,
            transmitter_class,
            local_version_remote_store,
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

    if log_file is not None:
        logger = JSONLogger(path=log_file)
        optimizer.subscribe(Events.OPTIMIZATION_STEP, logger)
        screen_logger = ScreenLogger()
        optimizer.subscribe(Events.OPTIMIZATION_START, screen_logger)
        optimizer.subscribe(Events.OPTIMIZATION_STEP, screen_logger)
        optimizer.subscribe(Events.OPTIMIZATION_END, screen_logger)

    optimizer.maximize(
        init_points=init_point,
        n_iter=n_iter,
    )
    print("Optimal chunk size: {}".format(optimizer.max))
    return int(optimizer.max["params"]["chunk_size"])
