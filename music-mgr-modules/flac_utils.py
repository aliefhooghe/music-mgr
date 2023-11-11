# -*- coding: utf-8 -*-

import subprocess as sb
import config
from string import digits

#   metaflac wrapper

def parse_int(input: str):
	separators = [ '/' ]
	
	for sep in separators:
		if sep in input:
			return int(input.split(sep)[0])
		
	return int(input)

class metadata:

	__tags = [
		("album", str),
		("albumartist", str),
		("artist", str),
		("composer", str),
		("date", str),
		("description", str),
		("discnumber", parse_int),
		("disctotal", parse_int),
		("genre", str),
		("title", str),
		("tracknumber", parse_int),
		("tracktotal", parse_int)
	]

	def __init__(self, flac_path):
		self.flac_path = flac_path
		raw_tags = metadata._get_all_tags_raw(flac_path)
		for tag in self.__tags:
			tag_name = tag[0]
			tag_type = tag[1]
			tag_value = metadata._type_tag(raw_tags.get(tag_name), tag_type)
			setattr(self, tag_name, tag_value)

	def __str__(self):
		description = "{} FLAC metadatas:\n".format(self.flac_path)

		for tag in self.__tags:
			tag_name = tag[0]
			tag_value = getattr(self, tag[0])
			if tag_value is not None:
				description += "    {}\t:\t{}\n".format(tag_name, tag_value)

		return description

	def _get_all_tags_raw(path):
		output = sb.check_output([config.METAFLAC_PATH, "--export-tags-to=-", path])
		lines = output.decode('UTF-8').splitlines()
		
		tag_dict = {}

		for line in lines:
			# Ignore multiline tags
			if '=' in line:
				key, _, value = line.partition('=')
				tag_dict[key.lower()] = value.lstrip().rstrip()
			
		return tag_dict

	def _type_tag(tag, type = str):
		return None if (tag is None or tag == "") else type(tag)

#   flac wrapper

def __encode_command(from_path, to_path, compression_level):
	return [config.FLAC_PATH, "-" + str(compression_level), "--totally-silent", from_path, "-o", to_path]

def __decode_comand(from_path, to_path):
	return [config.FLAC_PATH, "-d", "--totally-silent", from_path, "-o", to_path]

def encode(from_path, to_path, compression_level = 8):
    sb.check_output(__encode_command(from_path, to_path, compression_level))

def decode(from_path, to_path):
	sb.check_output(__decode_comand(from_path, to_path))

# async flac wrappers

def async_encode(from_path, to_path, compression_level = 8):
	return sb.Popen(__encode_command(from_path, to_path, compression_level), stdout = sb.PIPE)

def async_decode(from_path, to_path):
	return sb.Popen(__decode_comand(from_path, to_path), stdout = sb.PIPE)

#   shnsplit wrapper
def cue_split(flac_file, cue_file, output_dir):
    sb.call([config.SHNSPLIT_PATH, "-f", cue_file, "-t", "%n %t", "-o", "wav", "-d", output_dir, flac_file, "-P", "none"])
