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
		if (child.get("name") != "Files" and child.get("name") != "Input Files"):
			for child in child:
				paramName = child.get("name")
				params.append(paramName)
	comLine(name, toolFileName, inputs, params, outputPresent) 

	#Convert isis inputs to galaxy format
	inputs = []
	inputFileType = []
	for child in root.find("groups").find("group"):
		if (child.get("name") != "TO" and child.find("type").text != "boolean"):
			inputs.append(child.get("name"))
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
	convertParams(inputFile, toolFileName)

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
		if temp == "FROM":
			inputString += temp + "=$input "
		elif temp == "TO":
			inputString += temp + "=$output "
		else:
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
	inputName = list(reversed(inputName))
	inputType = list(reversed(inputType))
	galaxyFile = open(toolFile, "a")
	inputStart = '\n\t<inputs>'
	galaxyFile.write(inputStart)
	while len(inputName) > 0:
		curName = inputName.pop()
		curType = inputType.pop()
		temp = curType.split()
		if len(temp) > 1:
			temp1 = temp.pop()
			temp1 = temp1[2:]
			curType = temp1 + ',' + temp.pop()
		if curName == "TO":
			pass
		elif curName == "FROM":
			inputs = '\n\t\t<param name="input" format="' + curType + '" type="data" label="' + curName + '="/>'
			galaxyFile.write(inputs)
		else:
			inputs = '\n\t\t<param name="' + curName + '" format="' + curType + '" type="data" label="' + curName + '=" optional="true"/>' 
			galaxyFile.write(inputs)		
	galaxyFile.close()


#Convert Params
def convertParams(inputFile, toolFile):
	galaxyFile = open(toolFile, "a")
	tree = ET.parse(inputFile)
	root = tree.getroot()
	for child in root.find("groups"):
		if (child.get("name") != "Files" and child.get("name") != "Input Files"):
			gName = child.get("name")
			for child in child:
				pName = child.get("name")
				pType = ""
				pMin = ""
				pMax = ""
				pDefault = ""
				paramLine = ""
				if (child.find("type").text == "integer" or child.find("type").text == "double" or child.find("type").text == "float"):
					if (child.find("type").text) == "double":
						pType = "float"
					else:
						pType = child.find("type").text
					try:
						pMin = child.find("minimum").text
					except AttributeError:
						pMin = ""
					try:
						pMax = child.find("maximum").text
					except AttributeError:
						pMax = ""
					try:
						pDefault = child.find("internalDefault").text
					except AttributeError:
						try:
							pDefault = child.find("default").find("item").text
						except AttributeError:
							pDefault = ""
					if (pDefault == "Computed" or pDefault == "Internal Default" or pDefault == "Use default range" or pDefault == ""):
						if (pMin == "" and pMax == ""):
							paramLine = '\n\t\t<param name="' + pName + '" type="' + pType + '" optional="true"/>'
						elif (pMin != "" and pMax == ""):
							paramLine = '\n\t\t<param name="' + pName + '" type="' + pType + '" min="' + pMin + '" optional="true"/>'
						elif (pMin == "" and pMax != ""):
							paramLine = '\n\t\t<param name="' + pName + '" type="' + pType + '" max="' + pMax + '" optional="true"/>'
						else:
							paramLine = '\n\t\t<param name="' + pName + '" type="' + pType + '" min="' + pMin + '" max="' + pMax + '" optional="true"/>'
						galaxyFile.write(paramLine)
					else:
						if (pMin == "" and pMax == ""):
							paramLine = '\n\t\t<param name="' + pName + '" type="' + pType + '" value="' + pDefault + '"/>'
						elif (pMin != "" and pMax == ""):
							paramLine = '\n\t\t<param name="' + pName + '" type="' + pType + '" value="' + pDefault + '" min="' + pMin + '"/>'
						elif (pMin == "" and pMax != ""):
							paramLine = '\n\t\t<param name="' + pName + '" type="' + pType + '" value="' + pDefault + '" max="' + pMax + '"/>'
						else:
							paramLine = '\n\t\t<param name="' + pName + '" type="' + pType + '" value="' + pDefault + '" min="' + pMin + '" max="' + pMax + '"/>'
						galaxyFile.write(paramLine)
				elif (child.find("type").text == "boolean"):
					pType = child.find("type").text
					try:
						pDefault = child.find("internalDefault").text
						if (pDefault == "Computed" or "Internal Default" or "Use default range"):
							pDefault == ""
					except AttributeError:
						pDefault = child.find("default").find("item").text
					paramLine = '\n\t\t<param name="' + pName + '" type="' + pType + '" checked="' + pDefault.lower() + '" truevalue = "yes" falsevalue="no"/>'
					galaxyFile.write(paramLine)
				elif (child.find("type").text == "filename"):
					pType = "data"
					fileType = ""
					try:
						fileType = child.find("filter").text 
						fileType = fileType.strip()
						fileType = fileType[2:]
					except:
						fileType = ""
					paramLine = '\n\t\t<param name="'+ pName + '" format="' + fileType + '" type="' + pType + '" label="' + pName + '=" optional="true"/>'
					galaxyFile.write(paramLine)
				elif (child.find("type").text.lower() == "string"): #TODO Fix so URLs added
					pDefault = child.find("default").find("item").text
					try:
						if child.find("list"):
							paramLine = '\n\t\t<param name="' + pName + '" type="select" display="radio">'
							galaxyFile.write(paramLine)
							for child in child.find("list"):
								optionLine = ""
								optionValue = child.get("value")
								if optionValue == pDefault:
									optionLine = '\n\t\t\t<option value="' + optionValue + '" selected="true">' + optionValue + '</option>'
								else: 
									optionLine = '\n\t\t\t<option value="' + optionValue + '">' + optionValue + '</option>' 
								galaxyFile.write(optionLine)
							endParamLine = '\n\t\t</param>'
							galaxyFile.write(endParamLine)
					except AttributeError:
						pType = "text"
						paramLine = '\n\t\t<param name="' + pName + '" type="' + pType + '" value="' + pDefault + '"/>'				
	closeInput = '\n\t</inputs>'
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

	
