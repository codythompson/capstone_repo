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

def print_to_file(f, string):
    f.write(string + "\n")

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

    successful_list = []
    missing_app_list = []
    gen_error_list = []

    for path in paths:
#        print "Translating: %s" % path
        args = ["python", "xmlTranslator.py", path]
        sub_proc = subprocess.Popen(args)
        sub_proc.communicate()
        if sub_proc.returncode == missing_application_tag_code:
            missing_app_list.append(path)
#            print "ERROR: The XML file %s was missing the application tag and could not be translated!" % path
        elif sub_proc.returncode == general_translation_error_code:
            gen_error_list.append(path)
#            print "ERROR: There was an error translating the XML file: %s, this file could not be translated!" % path
        elif sub_proc.returncode == 0:
            successful_list.append(path)
        else:
            gen_error_list.append(path)
#            print "ERROR: There was an error translating the XML file: %s, this file could not be translated!" % path
    
    f = open("translation_results.txt", "w")

    if len(successful_list) > 0:
        print_to_file(f, "============================================================")
        print_to_file(f, "The following %i files were successfully translated." % len(successful_list))
        print_to_file(f, "------------------------------------------------------------")
        for path in successful_list:
            print_to_file(f, path)

    if len(missing_app_list) > 0:
        print_to_file(f, "============================================================")
        print_to_file(f, "The following %i files could NOT be translated." % len(missing_app_list))
        print_to_file(f, "These files were missing the 'application' tag.")
        print_to_file(f, "------------------------------------------------------------")
        for path in missing_app_list:
            print_to_file(f, path)

    if len(gen_error_list) > 0:
        print_to_file(f, "============================================================")
        print_to_file(f, "The following %i files could NOT be translated." % len(gen_error_list))
        print_to_file(f, "The translater encountered an exception while translating them.")
        print_to_file(f, "------------------------------------------------------------")
        for path in gen_error_list:
            print_to_file(f, path)

    f.close()

if __name__ == "__main__":
    main()
