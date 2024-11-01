import logging
import os


class IncorrectIndexFileName(ValueError):
    def __init__(self, message):
        self.message = message


def validate_index_name(index_file_name, file):
    if os.path.isdir(file):
        if index_file_name.endswith(".caibx"):
            raise IncorrectIndexFileName(
                "{} is directory! Index must be .caidx file".format(file)
            )
        elif not index_file_name.endswith(".caidx"):
            index_file_name += ".caidx"
    else:
        if index_file_name.endswith(".caidx"):
            raise IncorrectIndexFileName(
                "{} is directory! Index must be .caibx file".format(file)
            )
        elif not index_file_name.endswith(".caibx"):
            index_file_name += ".caibx"
    return index_file_name
