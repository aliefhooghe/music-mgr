# -*- coding: utf-8 -*-
import os, errno

#
#       Files utils
#

def get_files_names(dir_path):
    return [
        f for f in os.listdir(dir_path) 
        if os.path.isfile(os.path.join(dir_path, f))]

def safe_mkdir(path):
    # Create directory if it doesnt exist
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def has_extension(ext):
    return lambda path : path.endswith(ext)

#
#       Naming utils
#

def number_prefix(tracknumber):
	i = int(tracknumber)
	if (i >= 10):
		return str(i) + " "
	else:
		return "0" + str(i) + " "

def make_valid_filename(name):
    #   Here are windows system forbiden characters 
    #   This set is more restricitive than the Unix one
    forbiden_chars = {
        '<' : '(',
        '>' : ')',
        ':' : '-',
        '"' : '\'',
        '\\' : ' ', 
        '/' : ' ',
        '|' : '-',
        '?' : ' ',
        '*' : '-',
        '\n': ' '
    }
    char_replacer = lambda c : forbiden_chars.get(c, c)
    char_list = list(name)
    char_list = map(char_replacer, char_list)
    return "".join(char_list)