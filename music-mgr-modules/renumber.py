# -*- coding: utf-8 -*-
import os, string, argparse
import my_utils as utils

def renumber(dir_path):
    # get all filename in direcory
    filenames = utils.get_files_names(dir_path)

    # sort filenames
    filenames.sort()

    # Remove prefix
    number = 1
    for filename in filenames:
        number_prefix = utils.number_prefix(number)
        new_filename = number_prefix + filename.lstrip(string.digits + ".-" + string.whitespace)
        os.rename(
            os.path.join(dir_path, filename),
            os.path.join(dir_path, new_filename))
        print(filename + " --> " + new_filename)
        number = number + 1


# Expose functionality
command = "renumber"
main_function = renumber
arguments = ["directory"]
description = "Renumber a directory"
