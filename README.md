# TransferEfficiencyTool

## Installation

* Clone repo
```
git clone https://github.com/EkaterinaNikolaeva/TransferEfficiencyTool.git
```

* Install the delivery utilities

For example, for Debian and Ubuntu:

```
sudo apt install rsync casync
```

To install desync, use [manual](https://github.com/folbricht/desync?tab=readme-ov-file#installation)

## Configuration

Collect the resources you are researching. 

Configuration examples are in the `configs/` directory.

* `name` - name of the resource

* `cas_config` - config for delivery utilities using Content addressable storage technology
    * `local_cache_store` - directory for local cache chunks
    * `remote_storage` - location of the remote chunk storage in format `<utility name>: <storage>`. For example, `desync: 'http://127.0.0.1:8000/'`
    * `index_storage` - local directory of index files
    * `local_version_of_remote_storage` - local directory with the resources. Directory will be used in the `make` and `extract` commands.
    * `chunk_sizes` - chunk sizes that will be reserched (cache hit and delivery time)
* `versions` - list of versions in the format:
    *  `name` - the name of the version to be used in the plots
    * `src_path`
        * `local` - location version for the extract and make commands of casync/desync
        * locations for other utilies in the format
            `rsync`: source location for rsync
* `cas_transmitters` - a list of transmitters using content addressable storage (casync, desync)
* `other_transmitters` - a list of other transmitters
* `result_data_store` - the directory for text data
* `result_plot_store` - the directory for plots
* `dest_path` - template, location of the destination resource

## Usage

0. It may be useful to make the necessary remote repositories and index files for CAS transmitters in advance

```
python3 main.py --config-file <config_file> --only-chunking
```

1. Start the server that returns the remote chunks

```
cd chunk_server/

python3 chunk_server.py -s <remote-storage-location>
```

For example,

```
python3 chunk_server.py -s ../remote_storage/clickhouse/
```

2. Set up network restrictions. You can use [comcast](https://github.com/tylertreat/comcast) or [tc](https://linux.die.net/man/8/tc).

For example,

```
sudo tc qdisc replace dev lo root netem rate 10mbit
```

To stop network restrictions:

```
sudo tc qdisc del dev lo root
```

3. Start researching resource deliverers

```
python3 main.py --config-file <config-file>
```
If index files and remote storage are ready, you can use

```
python3 main.py --config-file <config-file> --only-deliver
```

Use flag `--verbose` to show all plots, without this flag all data and plots will be saved in the directories specified in the configuration file only.

If you want to count only cache hits, use the `--only-cache-hit` only 