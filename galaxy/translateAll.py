import sys
import fmatch
import os
import subprocess

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

def main():
    files_to_find = sys.argv[1:]
    cwd = os.getcwd()

    paths = []
    for filename in files_to_find:
        if os.path.split(filename)[0] == "":
            root_dir = cwd
        else:
            root_dir = filename[0]
            filename = filename[1]
        paths.extend(recursively_find_matching_files(root_dir, filename)

    for path in paths:
        print "Translating: %s" % path
        args = ["python", "xmlTranslator.py", path]
        sub_proc = subprocess.Popen(args)
        subprocess.communicate()
        print "Finsihed translating %s" % path

if __name__ == "__main__":
    main()
