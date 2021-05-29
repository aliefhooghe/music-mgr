# -*- coding: utf-8 -*-

import os
import my_utils as utils

def main(dir_path, sub_name):
    # get all filename in directory
    filenames = utils.get_files_names(dir_path)

    for filename in filenames:
        new_filename = filename.replace(sub_name, "")
        print(filename + " --> " + new_filename)
        os.rename(
            os.path.join(dir_path, filename),
            os.path.join(dir_path, new_filename))

# Expose functionality
command = "del-sub-name"
arguments = ["directory", "subname"]
description = "Delete a filename substring for each file in a given directory"
main_function = main