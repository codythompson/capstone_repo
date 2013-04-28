import sys
import fnmatch
import os

def recursively_find_matching_files(root_dir, matchby):
    """
    will grab all files matching the description passed in.
    will recurse into subdirectories
    
    os.walk will recurse into all sub directories
    fnmatch.filter will grab all files in the filenames list that match matchby 
        which can have an asterisk wild card, for example
        fnmatch.filter(filenames, "*.xml") will return all files ending with 
          .xml in the filenames list.
    """

    matches = []
    for root, dirnames, filenames in os.walk(root_dir):
        for filename in fnmatch.filter(filenames, matchby):
            matches.append(root + '/' + filename)
    return matches

#MAIN
files_to_find = sys.argv[1:]
root_dir = os.getcwd()

#for name/wildcard provided on the command line,
#find paths for that/those file(s)
paths = []
for filename in files_to_find:
    paths.extend(recursively_find_matching_files(root_dir, filename))

print repr(paths)
