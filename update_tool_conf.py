import os, sys

'''
Created by Isaac Pitterle

This file currently uses a hard-coded filename and XML filepath.
These all need to be retrieved dynamically based on the file passed in to the XML Translator.
'''



'''
This function 'inserts' a string into the tool_conf file by renaming the file (appending
'.bak' to preserve the file in case of errors) and then re-writing with the original
filename, since Python doesn't support actual insertion
'''
def insert(str,category):
	# Move original tool_conf.xml to tool_conf.xml.bak
	filename = "tool_conf.xml"
	os.rename(filename, filename + ".bak")
	with open(filename + ".bak") as backup:
		# Re-write tool_conf.xml
		with open(filename, "w") as tool_conf:
			# Find the relevant line again
			for line in backup:
				# If this line isn't the one we're interested in, write as-is
				if line.find(category) == -1:
					tool_conf.write(line)
				# If it is, write the line, then write the new tool line
				else:
					tool_conf.write(line)
					tool_conf.write(str)
	# If everything completes successfully, remove the backup file
	os.remove(filename + ".bak")

def intoToolConf(xml_file, category):
	filename = "tool_conf.xml"
	tool_conf = open(filename, "r+")
	category_found = False
	# Search the tool_conf file to determine whether the tool already exists in it
	for line in tool_conf:
		# If it does, print a message, close the file and exit
		if line.find(xml_file) != -1:
			category_found = True
			print("Tool '" + xml_file + "' already exists in tool_conf.xml")
			tool_conf.close()
			return

	tool_conf.seek(0)


	# Search line-by-line for the specified category in the tool_conf file
	for line in tool_conf:
		# If the line contains the category name...
		if line.find(category) != -1:
			category_found = True
			print("Inserting '" + xml_file + "' in category '" + category + "'")
			tool_conf.close()
			# Call the insert method, passing the XML filename
			insert("\t\t<tool file=\"ISISTools/" + xml_file + "\"/>\n",category)
			break

	# If the category doesn't already exist...
	if (category_found == False):
		# Create an ID using the category name, by replacing spaces with underscores
		category_id = ""
		for char in category:
			if char == ' ':
				category_id += '_'
			else:
				category_id += char

		# Jump to the end of the file and create the new category
		tool_conf.seek(-11,2)
		tool_conf.write("\n\t<section name=\"" + category + "\" " + "id=\"" + category_id + "\">")
		tool_conf.write("\n\t\t<tool file=\"" "ISISTools/"+ xml_file + "\"/>")
		tool_conf.write("\n\t</section>")
		tool_conf.write("\n</toolbox>")

	tool_conf.close()
