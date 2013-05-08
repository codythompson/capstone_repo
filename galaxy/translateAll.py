import sys
import fnmatch
import os
import subprocess

missing_application_tag_code = 42
general_translation_error_code = 43

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
        filename = os.path.split(filename)
        if filename[0] == "":
            root_dir = cwd
        else:
            root_dir = filename[0]
            filename = filename[1]
        paths.extend(recursively_find_matching_files(root_dir, filename))

    missing_app_list = []
    gen_error_list = []

    for path in paths:
        print "Translating: %s" % path
        args = ["python", "xmlTranslator.py", path]
        sub_proc = subprocess.Popen(args)
        sub_proc.communicate()
        if sub_proc.returncode == missing_application_tag_code:
            missing_app_list.append(path)
            print "ERROR: The XML file %s was missing the application tag and could not be translated!" % path
        elif sub_proc.returncode == general_translation_error_code:
            gen_error_list.append(path)
            print "ERROR: There was an error translating the XML file: %s, this file could not be translated!" % path

    print "============================================================"
    print "The following files could NOT be translated."
    print "These files were missing the 'application' tag."
    print "------------------------------------------------------------"
    for path in missing_app_list:
        print path

    print "============================================================"
    print "The following files could NOT be translated."
    print "The translater encountered an exception while translating them."
    print "------------------------------------------------------------"
    for path in gen_error_list:
        print path

if __name__ == "__main__":
    main()
