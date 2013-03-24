'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
xmlTranslator.py
v0.1

This module accepts an ISIS XML file and parses its contents
to create an equivalent Galaxy XML file. 

This module will then add the file into Galaxy automatically.

Created by Kolby Chien 27.2.2013
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import sys
import xml.etree.ElementTree as ET

#global variable storing command line args
commandLine = ""

#Parse ISIS XML file and generate galaxy XML file
def parseFile(inputFile):
	tree = ET.parse(inputFile)
	root = tree.getroot()
	name = root.get("name")

   	toolName(name)

	description = root.find("description").text
	toolDescribe(description)

	comLine(name) #TODO add parameters

	


	#f.close()

#Create a equivalent galaxy file
def createGalaxyFile():
	outputFile = ""
	temp = sys.argv[1]
	for char in temp:
		if char is ".":
			break
		else:
			outputFile += char
	galaxyFile = open(outputFile, "w")
			


#Convert tool name into galaxy format
def toolName(name):
	toolName = "<tool id=" + name + " name=" + name + ">"


#Convert Description
#TODO format text to remove intermediate tabs
def toolDescribe(text):
	toolDesc = "<description>" + text  + "</description>"


#Convert Command Line
#TODO add parameter functions
def comLine(name):
	comLine = "<command>isisToolExecutor.py " + name + " from=$input" + " to=$output</command>"


#Convert Input
#TODO test
def convertInput():
	fileInput = ""
	inputs = '<inputs>\n' + '<param format=' + fileInput + ' name="input" type="data" label="from="/>' +'\n</inputs>'
	print inputs

'''
#Convert Params
def convertParams():

#Convert Output
def convertOutput():
	outputs = '<outputs>\n' + '<data format=' + fileOutput + 'name="output" label="to"/>'

#Add help section
#TODO Text should refer to relavent isis website
def convertHelp(text):
	help = '<help>' + text + '</help>'

#Add tool to galaxy.
#Done after parsing
def toolToGalaxy():
'''

#createGalaxyFile()
parseFile(sys.argv[1])

	
