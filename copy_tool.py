import os, sys, shutil

######
# Created by Isaac Pitterle
#
# This file currently uses a hard-coded filename, section name (category)
# and partially hard-coded destination path.  These all need to be retrieved
# dynamically based on the file passed in to the XML Translator.
#
######

# TODO: Get these strings dynamically
target_file = ""
category = ""
destination = "galaxy/tools/" + category

shutil.copy(target_file, destination + "/" + target_file)
