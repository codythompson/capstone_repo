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

#Parse ISIS XML file and generate galaxy XML file
def parseFile(inputFile):
	tree = ET.parse(inputFile)
	root = tree.getroot()
	name = root.get("name")
	toolFileName = name

	#Determine tool name and create outer XML element
   	toolName(name, toolFileName)

	#Tool description
	description = root.find("brief").text
	toolDescribe(description, toolFileName)

	outputPresent = 1 #If there is an output, is 0, otherwise 1

	#Parses through xml file to find inputs and output 
	inputs = []
	params = []
	for child in root.find("groups").find("group"):
		#If an output file exists, set the flag
		if child.get("name") == "TO":
			outputPresent = 0
		inputName = child.get("name")
		inputs.append(inputName)
	for child in root.find("groups"):
		if child.get("name") != "Files":
			for child in child:
				paramName = child.get("name")
				params.append(paramName)
	comLine(name, toolFileName, inputs, params, outputPresent) 

	#Convert isis inputs to galaxy format
	inputFileType = []
	for child in root.find("groups").find("group"):
		try:
			inputType = child.find("filter").text
			inputType = inputType.strip()
			inputType = inputType[2:]
			inputFileType.append(inputType)
		except AttributeError:
			inputType = child.find("type").text
			if inputType == "cube":
				inputFileType.append("cub")
	convertInput(inputs, inputFileType, toolFileName)

	#Convert tool parameters to Galaxy
	paramType = []
	paramMin = []
	paramDefault = []
	for child in root.find("groups"):
		if child.get("name") != "Files":
			for child in child:
				paramName = child.get("name")
				params.append(paramName)
	convertParams(toolFileName)

	#Determine tool's output file type
	outputType = ""
	if outputPresent is 0:
		for child in root.find("groups").find("group"):
			if child.get("name") == "TO":
				try:
					outputType = child.find("filter").text
					outputType = outputType.strip()
					outputType = outputType[2:]
				except AttributeError:
					outputType = "cub"
	else:
		outputType = "cub"

	convertOutput(outputType, toolFileName)

	convertHelp(name, toolFileName)


#Create a equivalent galaxy file
def createGalaxyFile():
	if len(sys.argv) < 1:
		print "Usage: Accepts 1 xml file"
		exit()
	elif len(sys.argv) > 2:
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
def toolDescribe(text, toolFile):
	text = text.strip()
	toolDesc = '\n\t<description>' + text  + '</description>'
	galaxyFile = open(toolFile, "a")
	galaxyFile.write(toolDesc)
	galaxyFile.close()


#Convert Command Line
#TODO add parameter functions and fix if statement to check for output
def comLine(name, toolFile, inputs, params, outputPresent):
	#compile inputs and output files for command line
	inputString = ""
	inputs = list(reversed(inputs))
	while len(inputs) > 0:
		temp = inputs.pop()
		inputString += temp + "=$" + temp + ' '

	#compile params for command line
	paramString = ""
	params = list(reversed(params))
	while len(params) > 0:
		temp = params.pop()
		paramString += temp + "=$" + temp + ' '
	if outputPresent is 1:
		comLine = '\n\t<command interpreter="python">isisToolExecutor.py in_is_out=true to=$to start ' + name + ' ' + inputString + paramString + '</command>'
	else:
		comLine = '\n\t<command interpreter="python">isisToolExecutor.py ' + name + ' ' + inputString + paramString + '</command>'
	galaxyFile = open(toolFile, "a")
	galaxyFile.write(comLine)
	galaxyFile.close()


#Convert Input
def convertInput(inputName, inputType, toolFile):
	galaxyFile = open(toolFile, "a")
	inputs = '\n\t<inputs>'
	galaxyFile.write(inputs)
	for index in inputName:
		if index == "TO":
			pass
		else:
			for fileType in inputType:
				inputs = '\n\t\t<param name="' + index + '" format="' + fileType + '" type="data" label="from="/>'
				galaxyFile.write(inputs)
				break
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

#Adds help section to galaxy xml which refers user to relavent isis tool page
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

	
