import util.exec

from util.plot import make_plot, Subplot
from util.dump_data import safe_data_to_file
import os


def calculate_cache_hit(index_storage_dir, versions):
    files = os.listdir(index_storage_dir)
    version_names = dict()
    for file in files:
        version_names[file[: file.rfind(".")]] = file
    results = []
    existing_chunks = set()
    for version in versions:
        list_chunks = util.exec.run(
            [
                "desync",
                "list-chunks",
                os.path.join(index_storage_dir, version_names[version.name]),
            ]
        ).split("\\n")
        list_chunks.pop()
        cache_hit = 0
        for chunk in list_chunks:
            if chunk not in existing_chunks:
                existing_chunks.add(chunk)
            else:
                cache_hit += 1
        results.append(cache_hit / len(list_chunks))
    return results


def calculate_cache_hit_by_indexes(
    index_storage, versions, data_file=None, plot_file=None
):
    results = []
    index_dirs = []
    for file in os.listdir(index_storage):
        if os.path.isdir(os.path.join(index_storage, file)):
            index_dirs.append(int(file))
    index_dirs.sort()
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
