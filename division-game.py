#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, getopt, re, traceback
import divisionGamesClass as dg

usage = ("Calculates the NIM row of the given division game saves it in the file and plots"
"\nUsage: %s -d denumerators -n length [-m <b|u|d> -e end-position -f data-file-directory -t <key|all> -p plot-directory]"
"\n\t-d denumerators d1,d2,... (without spaces!), where di is a positive integer"
"\n\t-n length of the NIM row, positive integer"
"\n\t-m game mode:"
"\n\t\tb: (both) player can choose either to round up or down (default)"
"\n\t\tu: (up) rounding fractions up"
"\n\t\td: (down) rounding fractions down"
"\n\t-e end position, non-negative integer, typically 0 or 1 (default 1)"
"\n\t-f data file directory, defaults to './data/<mode>-<end-position>/', file name generated automatically: 'data-d<denumeratotrs><mode><end-position>-n=<length>.dat'"
"\n\t-t type of data:"
"\n\t\tkey: only key positions, where the NIM value changes (default)"
"\n\t\tall: all positions"
"\n\t-p plot directory, defaults to './plots/<mode>-<end-position>/', file name generated automatically: 'plt-d<denumeratotrs><mode><end-position>-n=<length>.pdf'"
) % sys.argv[0]

try:
	myopts, args = getopt.getopt(sys.argv[1:],"hd:n:m:e:f:t", ["help"])
except getopt.GetoptError as e:
	print (str(e))
	print(usage)
	sys.exit(2)

def main():
	for opt, arg in myopts:
		if opt in ("-h", "--help"):
			print(usage)
			sys.exit()
		elif opt == '-d': # dalītāji
			try:
				denums = re.split(',', arg)
			except Exception as e:
				print("Error while processing denumerators (-d): " + str(e))
		elif opt == '-n': # rindas garums
			try:
				n = int(arg)
			except Exception as e:
				print("Error while processing length (-n): " + str(e))
		elif opt == '-m': # spēles tips
			try:
				mode = str(arg)
			except Exception as e:
				print("Error while processing game mode (-m): " + str(e))
		elif opt == '-e': # beigu pozīcija
			try:
				ends = int(arg)
			except Exception as e:
				print("Error while processing end position (-e): " + str(e))
		elif opt == '-f': # datu faila direktorija
			try:
				dataDriectory = str(arg)
			except Exception as e:
				print("Error while processing data file directory (-f): " + str(e))
		elif opt == '-t': # datu faila tips
			try:
				dataMode = str(arg)
			except Exception as e:
				print("Error while processing data type (-t): " + str(e))
		elif opt == '-p': # grafika direktorija
			try:
				plotDirectory = str(arg)
			except Exception as e:
				print("Error while processing plot directory (-p): " + str(e))
		else:
			sys.exit(usage)

#	print(denums)
	
	# noklusētās vērtības	
	try:
		mode
	except NameError:
		mode = 'b'

	try:
		ends
	except NameError:
		ends = 1

	try:
		dataMode
	except NameError:
		dataMode = 'key'

	try:
		dataDirectory
	except NameError:
		dataDirectory = './data/' + str(mode) + '-' + str(ends) + '/'

	try:
		plotDirectory
	except NameError:
		plotDirectory = './plots/' + str(mode) + '-' + str(ends) + '/'


	# Exit when mandatory parameters are not defined
	try:
		n
	except NameError:
		sys.exit(usage)

	try:
		denums
	except Exception as e:
		sys.exit(usage)
	
	try:
		if not isinstance(denums, list):
			raise Exception("Invalid definition of denumerators!")

		for i, d in enumerate(denums):
			d = int(d)
			if not isinstance(d, int) or d < 1:
				raise Exception("Invalid definition of denumerator (-d) #" + str(i + 1) + " it must be a positive integer")
			denums[i] = d
		
		if not n > ends:
			raise Exception("Invalid row length (-n), it must be a positive integer, larger than the end position")
			
		if mode not in ['b','d','u']:
			raise Exception("Invalid game mode (-m), valid values: b, d or u")

		if not os.path.exists(dataDirectory):
			os.makedirs(dataDirectory)

		if not os.path.exists(plotDirectory):
			os.makedirs(plotDirectory)

	except Exception as e:
		print("Error: " + str(e))
		traceback.print_exc()
		print(usage)
		
	game = dg.divisionGame(denums, mode, ends)
	game.nimRow(n)
	game.plotNimRow(n, plotDirectory)
	game.saveNimRow(n, dataMode, dataDirectory)
		
	
if __name__ == "__main__":
	main()

