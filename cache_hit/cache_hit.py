import util.exec

from util.plot import make_plot
import os
import tempfile


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
                os.path.join(index_storage_dir, version_names[version]),
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


def calculate_cache_hit_by_indexes(index_storage, versions, plot_file):
    results = dict()
    for file in os.listdir(index_storage):
        if os.path.isdir(os.path.join(index_storage, file)):
            results[file] = calculate_cache_hit(
                os.path.join(index_storage, file), versions
            )
    make_plot("Cache hit", versions, results, plot_file=plot_file)
