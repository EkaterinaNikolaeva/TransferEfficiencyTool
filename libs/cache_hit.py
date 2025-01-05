import util.exec

from util.plot import make_plot, Subplot
from util.dump_data import safe_data_to_file
import os


def get_chunk_lists(index_storage_dir, versions):
    files = os.listdir(index_storage_dir)
    version_names = dict()
    for file in files:
        version_names[file[: file.rfind(".")]] = file
    chunks_lists = []
    for version in versions:
        list_chunks = util.exec.run(
            [
                "desync",
                "list-chunks",
                os.path.join(index_storage_dir, version_names[version.name]),
            ]
        ).split("\\n")
        list_chunks.pop()
        chunks_lists.append(list_chunks)
    return chunks_lists


def get_index_dirs(index_storage, chunk_sizes):
    index_dirs = []
    for file in os.listdir(index_storage):
        if (
            os.path.isdir(os.path.join(index_storage, file))
            and int(file) in chunk_sizes
        ):
            index_dirs.append(int(file))
    index_dirs.sort()
    return index_dirs


def calculate_cache_hit(index_storage_dir, versions):
    chunks_lists = get_chunk_lists(index_storage_dir, versions)
    results = []
    existing_chunks = set()
    for list_chunks in chunks_lists:
        cache_hit = 0
        for chunk in list_chunks:
            if chunk not in existing_chunks:
                existing_chunks.add(chunk)
            else:
                cache_hit += 1
        results.append(cache_hit / len(list_chunks))
    return results


def calculate_cache_hit_by_indexes(
    chunk_sizes, index_storage, versions, data_file=None, plot_file=None
):
    results = []
    index_dirs = get_index_dirs(index_storage, chunk_sizes)
    for dir in index_dirs:
        results.append(
            Subplot(
                name=str(dir),
                data=calculate_cache_hit(
                    os.path.join(index_storage, str(dir)), versions
                ),
            )
        )
    if data_file is not None:
        safe_data_to_file(data_file, results)
    if plot_file is not None:
        make_plot(
            "Cache hit",
            [version.name for version in versions],
            results,
            plot_file=plot_file,
            xlabel="Version",
            ylabel="Cache hit",
        )
    return results


def find_average_cache_hit(cache_hit):
    return sum(cache_hit[1:]) / (len(cache_hit) - 1)


def calculate_average_cache_hit(
    cache_hits, chunk_sizes, data_file=None, plot_file=None
):
    average_cache_hits = []
    for i in range(len(chunk_sizes)):
        average_cache_hits.append(find_average_cache_hit(cache_hits[i].data))
    if data_file is not None:
        safe_data_to_file(data_file, average_cache_hits)
    if plot_file is not None:
        make_plot(
            "Average cache hit",
            chunk_sizes,
            [Subplot("", average_cache_hits)],
            plot_file=plot_file,
            xlabel="Chunk size",
            ylabel="Cache hit",
        )
    return average_cache_hits


def calculate_importance_last_version(index_storage_dir, versions):
    chunks_lists = get_chunk_lists(index_storage_dir, versions)
    common_cache_hit = []
    prev_cache_hit = []
    existing_chunks = set()
    prev_chunks = set()
    current_chunks = set()
    for list_chunks in chunks_lists:
        cache_hit = 0
        cache_hit_prev_version = 0
        for chunk in list_chunks:
            if chunk not in existing_chunks:
                existing_chunks.add(chunk)
            else:
                cache_hit += 1
            if chunk in prev_chunks or chunk in current_chunks:
                cache_hit_prev_version += 1
            current_chunks.add(chunk)
        common_cache_hit.append(cache_hit / len(list_chunks))
        prev_cache_hit.append(cache_hit_prev_version / len(list_chunks))
        prev_chunks = current_chunks.copy()
        current_chunks = set()
    results = []
    for i in range(len(versions)):
        if common_cache_hit[i] == 0:
            ratio = 1
        else:
            ratio = prev_cache_hit[i] / common_cache_hit[i]
        results.append(ratio)
    return results


def calculate_importance_last_version_by_indexes(
    chunk_sizes, index_storage, versions, data_file=None, plot_file=None
):
    index_dirs = get_index_dirs(index_storage, chunk_sizes=chunk_sizes)
    results = []
    for dir in index_dirs:
        results.append(
            Subplot(
                name=str(dir),
                data=calculate_importance_last_version(
                    os.path.join(index_storage, str(dir)), versions
                ),
            )
        )
    if data_file is not None:
        safe_data_to_file(data_file, results)
    if plot_file is not None:
        make_plot(
            "Ratio of the importance of the latest version",
            [version.name for version in versions],
            results,
            plot_file=plot_file,
            xlabel="Version",
            ylabel="Cache hit",
        )
