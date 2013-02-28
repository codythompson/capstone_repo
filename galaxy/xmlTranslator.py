'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
xmlTranslator.py
v0.1

This module accepts an ISIS XML file and parses its contents
to create an equivalent Galaxy XML file. 

This module will then add the file into Galaxy automatically.

Created by Kolby Chien 27.2.2013
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#global variable storing command line args
commandLine = ""

#Parse ISIS XML file and generate galaxy XML file
def parseFile(inputFile):
	f = open(inputFile, "r")
	f.close()

#Convert tool name
def toolName():

#Convert Description
def toolDescribe():

#Convert Input
def convertInput():

#Convert Output
def convertOutput():

#Convert Params
def convertParams():

#Add tool to galaxy.
#Done after parsing
def toolToGalaxy():
	
