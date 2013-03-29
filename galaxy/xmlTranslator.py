'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
xmlTranslator.py
v0.5

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
	toolFileName = name

   	toolName(name, toolFileName)

	description = root.find("brief").text
	toolDescribe(description, toolFileName)

	outputPresent = 1 #If there is an output, is 0, otherwise 1

	#Parses through parameters to find if there is an output file.  
	for child in root.find("groups").find("group"):
		if child.get("name") == "TO":
			outputPresent = 0
	comLine(name, toolFileName, outputPresent) #TODO add parameters

	inputType = ""
	for child in root.find("groups").find("group"):
		if child.get("name") == "FROM":
			inputType = child.find("filter").text
			inputType = inputType.strip()
	inputType = inputType[2:]

	convertInput(inputType, toolFileName)

	convertParams(toolFileName)

	outputType = ""
	if outputPresent is 0:
		for child in root.find("groups").find("group"):
			if child.get("name") == "TO":
				outputType = child.find("filter").text
				outputType = outputType.strip()
		outputType = outputType[2:]
	else:
		outputType = "cub"

	convertOutput(outputType, toolFileName)

	convertHelp(name, toolFileName)


#Create a equivalent galaxy file
def createGalaxyFile():
	if len(sys.argv) < 1:
		print "Usage: Accepts 1 xml file"
		exit()
	elif len(sys.argv) > 1:
		print "Usage: Accepts 1 xml file"
		exit()
	else:
		outputFile = sys.argv[1]
		outputFile = outputFile[:-4]
		galaxyFile = open(outputFile, "w")
		galaxyFile.close()
			


#Convert tool name into galaxy format
def toolName(name, toolFile):
	toolName = '<tool id="' + name + '" name="' + name + '">'
	galaxyFile = open(toolFile, "w")
	galaxyFile.write(toolName)
	galaxyFile.close()


#Convert Description
#TODO format text to remove intermediate tabs
def toolDescribe(text, toolFile):
	text = text.strip()
	toolDesc = '\n\t<description>' + text  + '</description>'
	galaxyFile = open(toolFile, "a")
	galaxyFile.write(toolDesc)
	galaxyFile.close()


#Convert Command Line
#TODO add parameter functions and fix if statement to check for output
def comLine(name, toolFile, outputPresent):
	if outputPresent is 1:
		comLine = '\n\t<command interpreter="python">isisToolExecutor.py in_is_out=true to=$to start ' + name + ' from=$input</command>'
	else:
		comLine = '\n\t<command interpreter="python">isisToolExecutor.py ' + name + ' from=$input' + ' to=$output</command>'
	galaxyFile = open(toolFile, "a")
	galaxyFile.write(comLine)
	galaxyFile.close()


#Convert Input
#TODO test
def convertInput(inputType, toolFile):
	inputs = '\n\t<inputs>\n' + '\t\t<param format="' + inputType + '" name="input" type="data" label="from="/>'
	galaxyFile = open(toolFile, "a")
	galaxyFile.write(inputs)
	galaxyFile.close()


#Convert Params
def convertParams(toolFile):
	closeInput = '\n\t</inputs>'
	galaxyFile = open(toolFile, "a")
	galaxyFile.write(closeInput)
	galaxyFile.close()


#Convert Output
def convertOutput(outputType, toolFile):
	outputs = '\n\t<outputs>\n' + '\t\t<data format="' + outputType + '" name="output" label="to"/>' + '\n\t</outputs>'
	galaxyFile = open(toolFile, "a")
	galaxyFile.write(outputs)
	galaxyFile.close()

#Add help section
#TODO Text should refer to relavent isis website
def convertHelp(tool,toolFile):
	help = '\n\t<help>isis.astrogeology.usgs.gov/Application/presentation/Tabbed/' + tool + '/' + tool + '.html</help>' + '\n</tool>'
	galaxyFile = open(toolFile, "a")
	galaxyFile.write(help)
	galaxyFile.close()

'''
#Add tool to galaxy.
#Done after parsing
def toolToGalaxy():
'''

createGalaxyFile()
parseFile(sys.argv[1])

	
