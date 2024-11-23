import yaml


def safe_data_to_file(file_name, data):
    with open(file_name, "w") as f:
        yaml.dump(data, f)
