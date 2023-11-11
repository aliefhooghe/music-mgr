

import os
from os import path
import flac_utils as flac
import my_utils as utils

def exec_parallel_encode_tasks(tasks):
    process = []
    for wav_path, flac_path in tasks:
        print(wav_path + " --> " + flac_path)
        flac_dir = path.dirname(flac_path)
        utils.safe_mkdir(flac_dir)
        process.append(flac.async_encode(wav_path, flac_path, 8))

    for p in process:
        p.wait()

def main(input_dir, output_dir, parallel_encode_count = 16):
    input_content = os.walk(input_dir)

    print("Saving input directory '" + input_dir + "' to output directory '" + output_dir + "'")

    parallel_encode_count = int(parallel_encode_count)
    tasks = []

    for (sub_dir, dir_list, file_list) in input_content:
        print("# Listing '" + sub_dir + "'")
        wav_list = filter(utils.has_extension(".wav"), file_list)

        for wav_file in wav_list:
            wav_path = path.join(sub_dir, wav_file)
            flac_path = path.splitext(path.join(output_dir, wav_path))[0] + ".flac"

            tasks.append((wav_path, flac_path))

            if (len(tasks) >= parallel_encode_count):
                exec_parallel_encode_tasks(tasks)
                tasks = []

    # At the end finnish remaining tasks
    exec_parallel_encode_tasks(tasks)

# Expose functionality
command = "backup"
arguments = ["input-dir", "output-dir"]
description = "Backup a wav directory"
main_function = main