'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
xmlTranslator.py
v1.0

This module accepts an ISIS XML file and parses its contents
to create an equivalent Galaxy XML file. 

This module will then add the file into Galaxy automatically.

Created by Kolby Chien 27.2.2013
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import sys, os, shutil
import xml.etree.ElementTree as ET
from update_tool_conf import *

#Parse ISIS XML file and generate galaxy XML file
def parseFile(inputFile):
	#Take the xml tree from the isis xml file and retrieve the root tag
	tree = ET.parse(inputFile)
	root = tree.getroot()
	name = root.get("name") + ".xml"

	toolFileName = name #string file with the name of tool file

	#Determine tool name and create outer XML element
   	toolName(name, toolFileName)

	#Convert tool description
	description = root.find("brief").text
	toolDescribe(description, toolFileName)

	outputPresent = 1 #If there is an output, is 0, otherwise 1

	#Convert command line

	#Parses through xml file to find inputs and output 
	inputs = [] #array containing all param names under "Files" group
	params = [] #array containing all param names under all other groups

	#Get all input params and add them to inputs array for command line
	for child in root.find("groups").find("group"):
		#If an output file exists, set the flag
		if child.get("name") == "TO":
			outputPresent = 0
		inputName = child.get("name")
		inputs.append(inputName)

	exclusions = {}
	#Get param names for all other parameter groups for command line
	for child in root.find("groups"):
		if (child.get("name") != "Files" and child.get("name") != "Input Files"):
			for child in child:
				paramName = child.get("name")
				params.append(paramName)
				exclusionList = ""
				if child.find("exclusions"):
					for item in child.find("exclusions"):
						if exclusionList == "":
							exclusionList = item.text
						else:
							exclusionList = exclusionList + "," + item.text
					exclusions[paramName] = exclusionList
				elif child.find("list"):
					for child in child.find("list"):
						if child.find("exclusions"):
							for item in child.find("exclusions"):
								if exclusionList == "":
									exclusionList = item.text
								else:
									exclusionList = exclusionList + "," + item.text
							exclusions[paramName] = exclusionList
	comLine(name, toolFileName, inputs, params, outputPresent, exclusions) 

	#Convert isis inputs to galaxy format
	inputs = [] #array containing all param names under "Files" group
	inputFileType = [] #array containing input types of inputs 

	#Loop through "Files" group
	for child in root.find("groups").find("group"):
		if (child.get("name") != "TO" and child.find("type").text != "boolean"):
			inputs.append(child.get("name"))
			#Search for the file's input type. An exception will be thrown if the
			#"filter" tag does not exist, so catch it and search for right file type
			# via if else strings
			try:
				inputType = child.find("filter").text
				inputType = inputType.strip()
				inputType = inputType[2:]
				inputFileType.append(inputType)
			except AttributeError:
				if (child.find("type").text == "cube"):
					inputFileType.append("cub")
				else:
					inputFileType.append("none")
	convertInput(inputs, inputFileType, toolFileName)

	#Convert tool parameters to Galaxy
	convertParams(inputFile, toolFileName)

	#Determine tool's output file type
	outputType = ""
	#If there is a TO parameter, convert output type 
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

	#Convert a help section in galaxy
	#NOTE: Important for all galaxy files
	convertHelp(name, toolFileName)


#Create a galaxy file
def createGalaxyFile():
	#Check argument length
	if len(sys.argv) < 1:
		print "Usage: Accepts 1 xml file"
		exit()
	elif len(sys.argv) > 2:
		print "Usage: Accepts 1 xml file"
		exit()
	#Create file name in file, but with .gal extension
	else:
		inputPath = sys.argv[1]
		outputFile = os.path.split(inputPath)
		outputFile = outputFile[1]

		tree = ET.parse(inputPath)
		root = tree.getroot()
		if (root.tag.lower() == "application"):
			galaxyFile = open(outputFile, "w")
			galaxyFile.close()
		else:
			exit(42)
			


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
def comLine(name, toolFile, inputs, params, outputPresent, exclusions):
	#compile inputs and output files for command line
	inputString = ""
	#reverse list to pop first argument off first
	inputs = list(reversed(inputs)) 

	#While there are still elements in the list, Add them to the
	#input string for command line
	while len(inputs) > 0:
		temp = inputs.pop()
		if temp == "FROM":
			inputString += temp + "=$input "
		elif temp == "TO":
			inputString += temp + "=$output "
		else:
			inputString += temp + "=$" + temp + ' '

	#compile params for command line
	paramString = ""
	params = list(reversed(params))
	#While there are still elements in the param list, add
	#them to the param line string
	while len(params) > 0:
		temp = params.pop()
		paramString += temp + "=$" + temp + ' '

	#compile exclusion lists and arguments
	exclusionString = ""
	tempKey = exclusions.keys()
	tempVals = exclusions.values()
	i = 0
	while (i < len(tempKey)):
		exclusionString = exclusionString + 'exclusion="' + tempKey[i] + '=yes" ' + \
			 tempKey[i] + '="' + tempVals[i] + '" ' 
		i += 1

	#If there is a not a "TO" section, execute extra parameters 
	#in isisToolExecutor.py and then append inputs and params
	if outputPresent is 1:
		comLine = '\n\t<command interpreter="python">isisToolExecutor.py in_is_out=true to=$output ' + \
			exclusionString + 'start ' + name[:-4] + ' ' + inputString + paramString + '</command>'
	else:
		comLine = '\n\t<command interpreter="python">isisToolExecutor.py ' + exclusionString + 'start ' + \
			name[:-4] + ' ' + inputString + paramString + '</command>'
	galaxyFile = open(toolFile, "a")
	galaxyFile.write(comLine)
	galaxyFile.close()


#Convert Input
def convertInput(inputName, inputType, toolFile):
	#reverse lists so first input/param is popped first
	inputName = list(reversed(inputName))
	inputType = list(reversed(inputType))

	#open relavent tool file
	galaxyFile = open(toolFile, "a")
	
	#open input tag
	inputStart = '\n\t<inputs>'
	galaxyFile.write(inputStart)

	#For each input, create a param line in galaxy file
	while len(inputName) > 0:
		curName = inputName.pop()
		curType = inputType.pop()

		#split the file type to check if there are multiple
		#file types
		temp = curType.split()

		#If there are multiple file types, take off the "*."
		#and concatanate the types back together separated by 
 		#a ","
		if len(temp) > 1:
			temp1 = temp.pop()
			temp1 = temp1[2:]
			curType = temp1 + ',' + temp.pop()

		#skip output, process all else
		if curName == "TO":
			pass
		elif curName == "FROM":
			#If input does not have a "filter" tag, leave out a format
			if(curType == "none"):
				inputs = '\n\t\t<param name="input" type="data" label="' + curName + '="/>'
			else:
				inputs = '\n\t\t<param name="input" format="' + \
					curType + '" type="data" label="' + curName + '="/>'
			galaxyFile.write(inputs)
		else:
			#If input does not have a "filter" tag, leave out a format
			if(curType == "none"):
				inputs = '\n\t\t<param name="' + curName + \
					'" type="data" label="' + \
					curName + '=" optional="true"/>' 
			else:
				inputs = '\n\t\t<param name="' + curName + \
					'" format="' + curType + '" type="data" label="' + \
					curName + '=" optional="true"/>' 
			galaxyFile.write(inputs)		
	galaxyFile.close()


#Convert Params
def convertParams(inputFile, toolFile):
	#open galaxy file and retrieve the isis xml file tree
	galaxyFile = open(toolFile, "a")
	tree = ET.parse(inputFile)
	root = tree.getroot()

	#Loop through all parameter groups
	for child in root.find("groups"):
		if (child.get("name") == "Files" or child.get("name") == "Input Files"):
			for child in child:
				if (child.find("type").text == "boolean"):
					pName = child.get("name")
					pType = child.find("type").text
					pDefault = child.find("default").find("item").text
					try:
						pDefault = child.find("internalDefault").text
						if (pDefault == "Computed" or "Internal Default" 
							or "Use default range"):
							pDefault == ""
					except AttributeError:
						pDefault = child.find("default").find("item").text

					paramLine = '\n\t\t<param name="' + pName + \
						'" type="' + pType + '" checked="' + \
						pDefault.lower() + '" truevalue = "yes" falsevalue="no"/>'
					galaxyFile.write(paramLine)
		elif (child.get("name") != "Files" and child.get("name") != "Input Files"):
			gName = child.get("name")
			for child in child:
				pName = child.get("name") #string, parameter name
				pType = "" #string, parameter type (boolean, integer, etc.)
				pMin = "" #string, parameter minimum value (integer/float)
				pMax = "" #string, parameter maximum value (integer/float)
				pDefault = "" #string, parameter default value
				paramLine = "" #string, parameter line in galaxy

				#check for numerical parameter types
				if (child.find("type").text == "integer" 
					or child.find("type").text == "double" 
					or child.find("type").text == "float"):
					#Galaxy does not support double
					if (child.find("type").text) == "double":
						pType = "float"
					else:
						pType = child.find("type").text
					#try to find a minimum value
					try:
						pMin = child.find("minimum").text
					except AttributeError:
						pMin = ""
					#try to find a max value
					try:
						pMax = child.find("maximum").text
					except AttributeError:
						pMax = ""
					#try to find default value
					try:
						pDefault = child.find("internalDefault").text
					except AttributeError:
						try:
							pDefault = child.find("default").find("item").text
						except AttributeError:
							pDefault = ""
					#If default value is to use an internal default or computed, leave off value
					if (pDefault == "Computed" 
						or pDefault == "Internal Default" 
						or pDefault == "Use default range" 
						or pDefault == ""):
						#no min or max
						if (pMin == "" and pMax == ""):
							paramLine = '\n\t\t<param name="' + \
								pName + '" type="' + \
								pType + '" optional="true"/>'
						#Min exists, No max
						elif (pMin != "" and pMax == ""):
							paramLine = '\n\t\t<param name="' + \
								pName + '" type="' + pType + \
								'" min="' + pMin + \
								'" optional="true"/>'
						#No min, max exists
						elif (pMin == "" and pMax != ""):
							paramLine = '\n\t\t<param name="' + \
								pName + '" type="' + pType + \
								'" max="' + pMax + '" optional="true"/>'
						#Min and max exist
						else:
							paramLine = '\n\t\t<param name="' + \
								pName + '" type="' + pType + \
								'" min="' + pMin + '" max="' + \
								pMax + '" optional="true"/>'
						galaxyFile.write(paramLine)
					#Default value is not "computed" or "internal default" etc.
					else:
						if (pMin == "" and pMax == ""):
							paramLine = '\n\t\t<param name="' + \
								pName + '" type="' + pType + \
								'" value="' + pDefault + '"/>'
						elif (pMin != "" and pMax == ""):
							paramLine = '\n\t\t<param name="' + \
								pName + '" type="' + pType + \
								'" value="' + pDefault + \
								'" min="' + pMin + '"/>'
						elif (pMin == "" and pMax != ""):
							paramLine = '\n\t\t<param name="' + \
								pName + '" type="' + pType + \
								'" value="' + pDefault + \
								'" max="' + pMax + '"/>'
						else:
							paramLine = '\n\t\t<param name="' + \
								pName + '" type="' + pType + \
								'" value="' + pDefault + \
								'" min="' + pMin + '" max="' + pMax + '" optional="true"/>'
						galaxyFile.write(paramLine)
				#param type is boolean
				elif (child.find("type").text == "boolean"):
					pType = child.find("type").text
					try:
						pDefault = child.find("internalDefault").text
						if (pDefault == "Computed" or "Internal Default" 
							or "Use default range"):
							pDefault == ""
					except AttributeError:
						pDefault = child.find("default").find("item").text
					paramLine = '\n\t\t<param name="' + pName + \
						'" type="' + pType + '" checked="' + \
						pDefault.lower() + '" truevalue = "yes" falsevalue="no"/>'
					galaxyFile.write(paramLine)
				#param type is file
				elif (child.find("type").text == "filename"):
					pType = "data"
					fileType = ""
					try:
						fileType = child.find("filter").text 
						fileType = fileType.strip()
						fileType = fileType[2:]
					except:
						fileType = ""
					paramLine = '\n\t\t<param name="'+ pName + \
						'" format="' + fileType + '" type="' + \
						pType + '" label="' + pName + '=" optional="true"/>'
					galaxyFile.write(paramLine)
				#param type is string
				elif (child.find("type").text.lower() == "string"): 
					pDefault = child.find("default").find("item").text
					#Check if list exists, if so, param is a radio button list
					if child.find("list"):
						paramLine = '\n\t\t<param name="' + pName + '" type="select" display="radio">'
						galaxyFile.write(paramLine)
						#find all list options and write them to galaxy file
						for child in child.find("list"):
							optionLine = ""
							optionValue = child.get("value")
							if optionValue == pDefault:
								optionLine = '\n\t\t\t<option value="' + \
									optionValue + '" selected="true">' + \
									optionValue + '</option>'
							else: 
								optionLine = '\n\t\t\t<option value="' + \
									optionValue + '">' + optionValue + '</option>' 
							galaxyFile.write(optionLine)
						endParamLine = '\n\t\t</param>' #End param for options
						galaxyFile.write(endParamLine)
						#Not a list 
					else:
						paramLine = '\n\t\t<param name="' + pName + '" type="text" ' + \
							'value="' + pDefault + '"/>'
						galaxyFile.write(paramLine)
				#Child type is a file input
				elif (child.find("fileMode").text == "input"):
					pType = "data"
					fileType = child.find("filter").text
					fileType = fileType.strip()
					fileType = fileType[2:]
					paramLine = '\n\t\t<param name="'+ pName + \
						'" format="' + fileType + '" type="' + \
						pType + '" label="' + pName + '=" optional="true"/>'
					galaxyFile.write(paramLine)
				else:
					print pName
	closeInput = '\n\t</inputs>'
	galaxyFile.write(closeInput)
	galaxyFile.close()


#Convert Output
def convertOutput(outputType, toolFile):
	outputs = '\n\t<outputs>\n' + '\t\t<data format="' + outputType + \
		'" name="output" label="to"/>' + '\n\t</outputs>'
	galaxyFile = open(toolFile, "a")
	galaxyFile.write(outputs)
	galaxyFile.close()

#Adds help section to galaxy xml which refers user to relavent isis tool page
def convertHelp(tool,toolFile):
	help = '\n\t<help>isis.astrogeology.usgs.gov/Application/presentation/Tabbed/' + \
		tool + '/' + tool + '.html</help>' + '\n</tool>'
	galaxyFile = open(toolFile, "a")
	galaxyFile.write(help)
	galaxyFile.close()


#Add tool to galaxy.
#Done after parsing
def toolToGalaxy():
	inputFile = os.path.split(sys.argv[1]) #user input
	galXMLFile = inputFile[1] #user file
	destination = "tools/ISISTools" #directory file installed to
	script = "isisToolExecutor.py" #Name of the intermediary script

	#Check to see if the ISISTools directory exists, if
	#not, create it and add in the intermediary script
	if not os.path.exists(destination):
		os.mkdir(destination)
		shutil.copy(script,destination)
	#Copy Galaxy XML file and isis tool to directory
	shutil.copy(galXMLFile, destination) 

	#Get xml tree from ISIS xml file to searcy for category
	tree = ET.parse(sys.argv[1])
	root = tree.getroot()
	
	#Get all categories for that tool and install into tool_conf.xml
	for child in root.find("category"):
		category = (child.text).replace(' ','_')
		intoToolConf(galXMLFile,category)
		
	#Finish by removing the duplicate Galaxy XML file left
	#in the main galaxy folder
	os.remove(galXMLFile)



#Run tool
def main():
	try:
		createGalaxyFile()
		parseFile(sys.argv[1])
		toolToGalaxy()
	except:
		exit(43)
main()
