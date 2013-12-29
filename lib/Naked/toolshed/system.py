#!/usr/bin/env python

import sys
import os

#------------------------------------------------------------------------------
#
# FILE & DIRECTORY PATHS
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# [ filename function ] (string)
#   returns file name from a file path (including the file extension)
#------------------------------------------------------------------------------
def filename(filepath):
	return os.path.basename(filepath)

#------------------------------------------------------------------------------
# [ file_extension function ] (string)
#   returns file extension from a filepath
#------------------------------------------------------------------------------
def file_extension(filepath):
	return os.path.splitext(filepath)

#------------------------------------------------------------------------------
# [ directory function ] (string)
#  returns directory path to the filepath
#------------------------------------------------------------------------------
def directory(filepath):
	return os.path.dirname(filepath)

#------------------------------------------------------------------------------
#  [ make_path function ] (string)
#   returns OS independent file path from tuple of path components
#------------------------------------------------------------------------------
def make_path(*path_list):
	return os.path.join(*path_list)

#------------------------------------------------------------------------------
#  [ currentdir_to_basefile decorator function ] (returns decorated original function)
#    adds the full working directory path to the basename of file in the first argument of the undecorated function
#------------------------------------------------------------------------------
def currentdir_to_basefile(func):
	from functools import wraps

	@wraps(func)
	def wrapper(file_name, *args, **kwargs):
		current_directory = os.getcwd() #get current working directory path
		full_path = os.path.join(current_directory, file_name) # join cwd path to the filename for full path
		return func(full_path, *args, **kwargs) #return the original function with the full path to file as first argument
	return wrapper

#------------------------------------------------------------------------------
# [ currentdir_firstargument decorator function ] (returns decorated original function)
#   adds the current working directory as the first function argument to the original function
#------------------------------------------------------------------------------
def currentdir_firstargument(func):
	from functools import wraps

	@wraps(func)
	def wrapper(dir="", *args, **kwargs):
		current_directory = os.getcwd()
		return func(current_directory, *args, **kwargs)
	return wrapper

#------------------------------------------------------------------------------
# [ currentdir_lastargument decorator function ] (returns decorated original function)
#   adds the current working directory as the last function argument to the original function
#   Note: you cannot use other named arguments in the original function with this decorator
#   Note: the current directory argument in the last position must be named current_dir
#------------------------------------------------------------------------------
def currentdir_lastargument(func):
	from functools import wraps

	@wraps(func)
	def wrapper(*args, **kwargs):
		the_cwd = os.getcwd()
		return func(*args, current_dir=the_cwd)
	return wrapper

#------------------------------------------------------------------------------
#  [ fullpath function ] (string)
#    returns the full path to a filename that is in the current working directory
#    file_name = the basename of the file in the current working directory
#    	Example usage where test.txt is in working directory:
#			filepath = fullpath("test.txt")
#------------------------------------------------------------------------------
@currentdir_to_basefile # current directory decorator - adds the directory path up to the filename to the basefile name argument to original function
def fullpath(file_name):
	return file_name

#------------------------------------------------------------------------------
# [ cwd function ] (string)
#   returns the current working directory path
#   does not need to be called with an argument, the decorator assigns it
#   	Example usage:
#       	current_dir = cwd()
#------------------------------------------------------------------------------
@currentdir_firstargument
def cwd(dir=""):
	return dir

#------------------------------------------------------------------------------
#
# FILE & DIRECTORY TESTING
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# [ file_exists function ] (boolean)
#  return boolean for existence of file in specified path
#------------------------------------------------------------------------------
def file_exists(filepath):
	return os.path.exists(filepath)

#------------------------------------------------------------------------------
# [ is_file function ] (boolean)
#  returns boolean for determination of whether filepath is a file
#------------------------------------------------------------------------------
def is_file(filepath):
	return os.path.isfile(filepath)

#------------------------------------------------------------------------------
# [ dir_exists function ] (boolean)
#   return boolean for existence of directory in specified path
#------------------------------------------------------------------------------
def dir_exists(dirpath):
	return os.path.exists(dirpath)

#------------------------------------------------------------------------------
# [ is_dir function ] (boolean)
#   returns boolean for determination of whether filepath is a directory
#------------------------------------------------------------------------------
def is_dir(filepath):
	return os.path.isdir(filepath)

#------------------------------------------------------------------------------
#
# FILE METADATA
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# [ filesize function ] (string)
#   return file size in bytes
#------------------------------------------------------------------------------
def file_size(filepath):
	return os.path.getsize(filepath)

#------------------------------------------------------------------------------
# [ mod_time function ] (string)
#   return the file modification date/time
#------------------------------------------------------------------------------
def file_mod_time(filepath):
	import time
	return time.ctime(os.path.getmtime(filepath))

#------------------------------------------------------------------------------
#
# FILE LISTINGS
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# [ list_all_files function ] (list)
#   returns a list of all files in developer specified directory
#------------------------------------------------------------------------------
def list_all_files(dir):
	filenames = [name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))]
	return filenames

#------------------------------------------------------------------------------
# [ list_filter_files function ] (list)
#   returns a list of files filtered by developer defined file extension in developer defined directory
#   	Usage example:
#   		filenames = list_filter_files("py", "tests")
#------------------------------------------------------------------------------
def list_filter_files(extension_filter, dir):
	if not extension_filter.startswith("."):
		extension_filter = "." + extension_filter #add a period if the developer did not include it
	filenames = [name for name in os.listdir(dir) if name.endswith(extension_filter)]
	return filenames

#------------------------------------------------------------------------------
# [ list_all_files_cwd function ] (list)
#   returns a list of all files in the current working directory
#   Note: does not require argument, the decorator assigns the cwd
#   	Usage example:
#			file_list = list_all_files_cwd()
#------------------------------------------------------------------------------
@currentdir_firstargument
def list_all_files_cwd(dir=""):
	return list_all_files(dir)

#------------------------------------------------------------------------------
# [ list_filter_files_cwd function ] (list)
#   returns a list of all files in the current working directory filtered by developer specified file extension
#	Note: do not specify the second argument, decorator assigns it
#   	Usage example:
#			file_list = list_filter_files_cwd(".py")
#------------------------------------------------------------------------------
@currentdir_lastargument
def list_filter_files_cwd(extension_filter, current_dir=""):
	return list_filter_files(extension_filter, current_dir)

#------------------------------------------------------------------------------
# [ list_match_files function ] (list)
#   returns a list of all files that match the developer specified match pattern
#	can optionally specify return of full path to the files (rather than relative path from cwd) by setting full_path to True
#   	Usage example:
#			file_list = list_match_files("*.py")
#			file_list_fullpath = list_match_files("*.py", True)
#------------------------------------------------------------------------------
def list_match_files(match_pattern, full_path = False):
	from glob import glob
	filenames = glob(match_pattern)
	if full_path:
		filenames_fullpath = []
		cwd = os.getcwd()
		for name in filenames:
			name = os.path.join(cwd, name) #make the full path to the file
			filenames_fullpath.append(name) #add to the new list
		return filenames_fullpath #then return that list
	else:
		return filenames

#------------------------------------------------------------------------------
#
# SYMBOLIC LINK TESTING
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# [ is_link function ] (boolean)
#   return boolean indicating whether the path is a symbolic link
#------------------------------------------------------------------------------
def is_link(filepath):
	return os.path.islink(filepath)

#------------------------------------------------------------------------------
# [ real_path function ] (string)
#   return the real file path pointed to by a symbolic link
#------------------------------------------------------------------------------
def real_path(filepath):
	return os.path.realpath(filepath)

#------------------------------------------------------------------------------
#
# DATA STREAMS
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# [ stdout function ]
#   print to std output stream
#------------------------------------------------------------------------------
def stdout(text):
	print(text)

#------------------------------------------------------------------------------
# [ stderr function ]
#   print to std error stream
#   optionally (i.e. if exit = nonzero integer) permits exit from application with developer defined exit code
#------------------------------------------------------------------------------
def stderr(text, exit=0):
	sys.stderr.write(text)
	if exit:
		raise SystemExit(exit)

#------------------------------------------------------------------------------
#
# APPLICATION CONTROL
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# [ exit_with_status function ]
#   application exit with developer specified exit status code (default = 1)
#------------------------------------------------------------------------------
def exit_with_status(exit=1):
	raise SystemExit(exit)

if __name__ == '__main__':
	pass