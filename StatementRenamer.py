#!/usr/bin/env python3

########################################################################

import PyPDF2
import re
import os
import shutil

########################################################################

########################################################################
# This program will traverse a list of downloaded CIBC Bank statements
# for both Chequing accounts and VISA Credit accounts and using the path
# specified in where you want it saved will rename the statement and save
# it with the correct name in the appropriate folder
########################################################################

# This method will return the rest of the string after specific key
def string_after(s, key):
	return s.partition(key)[2]

def main():

	# Set location for list of files to load and location to save files

	############################################
	## VALUE TO SET
	## Make sure to set this value to where
	## your list of statements is stored.
	pathToFiles = r"/home/user/Statements/"
	###########################################

	monthDict = {'Jan': '01','Feb': '02','Mar': '03','Apr': '04','May': '05','Jun': '06','Jul': '07','Aug': '08','Sep': '09','Oct': '10','Nov': '11','Dec': '12'}

	# Loop through files
	for pdf in os.listdir(pathToFiles):

		# Grab file name with location
		pdfFileName = pathToFiles + pdf
		# Create file object to stream
		pdfFileObj = open(pdfFileName, 'rb')
		# Read PDF
		pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict=False)
		# Grab the first page for overall info
		pageObj = pdfReader.getPage(0)
		# Grab text to parse from page
		textExtract = pageObj.extractText()

		# Statement is for Chequing account
		if(textExtract.find('Account Statement') != -1):
			textExtract = textExtract.split('.')

			# File name should be acct#_year_Month#MonthDay_to_MonthDay

			# Grab period of statement from list generated from split
			period = textExtract[2].split()
			# Grab account number
			acctNum = re.compile('[^a-z][0-9]-\d+').findall(period[7])[0]
			# Grab the year, month and date
			year = re.split('(\d+)', period[6])[1]
			monthInit = period[1]
			dayInit = period[2]
			monthEnd = period[4]
			dayEnd = period[5].split(',')[0]
			
			# Create final rename
			finalName = acctNum+"_"+year+"_"+monthDict[monthInit]+monthInit+dayInit+"_to_"+monthEnd+dayEnd+".pdf"
			finalDest = pathToFiles+finalName

			# Close PDF object and rename
			pdfFileObj.close()
			shutil.move(pdfFileName, finalDest)
			

		# Statement is for Credit account
		elif(textExtract.find('Your account at a glance') != -1):

			# File name depends on if statement in same year or not.
			# If not same year:
			# last4dig_firstYear_Month#MonthDay_to_MonthDay_secondYear
			# If same year:
			# last4dig_year_Month#MonthDay_to_MonthDay

			# Grab extract after 'Account number' to get info needed
			info = string_after(textExtract, "Account number")
			info.split(',')
			period = info.split()[:10]
			
			# Use period info and find pieces
			last4 = (re.split('(\d+)', period[3]))[1]
			firstMonth = re.split('period', period[5])[1][0:3]
			firstDate = re.split('(\d+)', period[6])[1]
			secondMonth = period[7][0:3]
			secondDate = re.split(',', period[8])[0]
			finalYear = re.split('(\d+)', period[9])[1]

			# Check to see if years are in same year (edge case)
			if(firstMonth == 'Dec'):
				firstYear = re.split('(\d+)', period[6])[3]
				finalName = (last4+"_"+firstYear+"_"+monthDict[firstMonth]+firstMonth+firstDate+"_to_"+secondMonth+secondDate+"_"+finalYear+".pdf")
			else:
				finalName = (last4+"_"+finalYear+"_"+monthDict[firstMonth]+firstMonth+firstDate+"_to_"+secondMonth+secondDate+".pdf")

			
			# Close PDF object and rename
			finalDest = pathToFiles+finalName
			pdfFileObj.close()
			shutil.move(pdfFileName, finalDest)

	print("Completed Renaming!!")


if __name__ == "__main__": main()