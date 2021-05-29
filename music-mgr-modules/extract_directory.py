# -*- coding: utf-8 -*-

import os, string
import os.path as path
import flac_utils as flac
import my_utils as utils


#
#   Single flac file extraction
#

def filename_from_metadata(metadata, ext):
    # Use track number as prefix if available
    filename_prefix = (
        utils.number_prefix(metadata.tracknumber) if metadata.tracknumber is not None
        else "")

    # Use filename as title if it is not provided in metadata
    title = (
        metadata.title if metadata is not None 
        else path.splitext(path.basename(metadata.flac_path))[0]
    ).title()

    return utils.make_valid_filename(filename_prefix + title + ext)

def album_directory_from_metadata(metadata):
    artist_folder = (
        metadata.albumartist if metadata.albumartist is not None 
        else metadata.artist if metadata.artist is not None
        else metadata.composer if metadata.composer is not None
        else "Unknown Artist"
    ).title()

    album_folder = (
        metadata.album if metadata.album is not None
        else "Unknown Album"
    ).title()

    if (metadata.discnumber is not None):
        if metadata.disctotal is None or metadata.disctotal is None > 1:
            album_folder = album_folder + " - Disc {}".format(metadata.discnumber)

    return path.join(
            utils.make_valid_filename(artist_folder),
            utils.make_valid_filename(album_folder))

def process_track(flac_path, output_dir):
    # Compute file path
    metadata = flac.metadata(flac_path)
    out_directory = path.join(output_dir, album_directory_from_metadata(metadata))
    out_filename = filename_from_metadata(metadata, ".wav")
    out_filepath = os.path.join(out_directory, out_filename)

    # Prepare directory
    utils.safe_mkdir(out_directory)

    # Convert file
    try:
        flac.decode(flac_path, out_filepath)
    except:
        print("ERROR: Faild to decode {} to {}".format(flac_path, out_filename))

    return out_filepath

#
#   CUE image extraaction
#

def cue_get_first_tag(lines, tag):
    try:
        line = next(l for l in lines if tag in l)
        strip_chars = string.whitespace + '"'
        return line.partition(tag)[2].lstrip(strip_chars).rstrip(strip_chars)
    except:
        return None

def process_cue_img(flac_path, cue_path, output_dir):
    with open(cue_path) as cue:
        cue_lines = cue.readlines()

    performer = cue_get_first_tag(cue_lines, "PERFORMER")
    title = cue_get_first_tag(cue_lines, "TITLE")
    composer = cue_get_first_tag(cue_lines, "COMPOSER")

    # define artist folder
    if (composer is not None):
        artist_folder = composer
    elif (performer is not None):
        artist_folder = performer
    else:
        artist_folder = "Unknown Artist"

    # define album folder
    if (title is not None):
        album_folder = title
    else:
        album_folder = "Unknown Album"

    album_directory = path.join(
        output_dir,
        utils.make_valid_filename(artist_folder),
        utils.make_valid_filename(album_folder))

    utils.safe_mkdir(album_directory)
    flac.cue_split(flac_path, cue_path, album_directory)

def main(input_dir, output_dir):
    print("Processing input directory '" + input_dir + "' to output directory '" + output_dir + "'")
    input_content = os.walk(input_dir)

    for (sub_dir, dir_list, file_list) in input_content:
        flac_list = list(filter(utils.has_extension(".flac"), file_list))
        cue_list = list(filter(utils.has_extension(".cue"), file_list))

        flac_count = len(flac_list)
        cue_count = len(cue_list)

        if (flac_count == 1 and cue_count == 1):
            print("## " + sub_dir + ": Image + cue")
            flac_path = path.join(sub_dir, flac_list[0])
            cue_path = path.join(sub_dir, cue_list[0])
            process_cue_img(flac_path, cue_path, output_dir)
        elif (flac_count > 0):
            print("## " + sub_dir + ": Separated flac tracks")
            for flac_file in flac_list:
                flac_path = os.path.join(sub_dir, flac_file)
                out_filepath = process_track(flac_path, output_dir)
                print("Converting [" + flac_file + "]" + " --> [" + out_filepath + "]")


# Expose functionality
command = "extract"
arguments = ["input-dir", "output-dir"]
description = "Extract a flac directory"
main_function = main