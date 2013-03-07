'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
xmlTranslator.py
v0.1

This module accepts an ISIS XML file and parses its contents
to create an equivalent Galaxy XML file. 

This module will then add the file into Galaxy automatically.

Created by Kolby Chien 27.2.2013
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import sys

#global variable storing command line args
commandLine = ""

#Parse ISIS XML file and generate galaxy XML file
def parseFile(inputFile):
	f = open(inputFile, "r") #open specified input file

	#Loop reads file line by line.  For each line, the first word is
	#read to determine whether it is a name, input, parameter, 
	#description, etc.
	for line in f.readlines():
		line.strip()
		words = line.split(" ")
		print words[0]
	f.close()

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
			

'''
#Convert tool name
def toolName()

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
'''

#createGalaxyFile()
parseFile(sys.argv[1])

	
