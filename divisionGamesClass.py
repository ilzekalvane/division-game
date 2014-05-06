# -*- coding: utf-8 -*-

import mex
import os
import sys

import matplotlib as mpl
mpl.use( "Agg" )

import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True

class divisionGame(object):
	'''
		Division game class, two arguments to initialize: 
			-denums: denumerators, Python list, example: [2,3,4]
			-mode: game mode, allowed values d, u, b
				* d (down) rounds fractions down
				* u (up) rounds fractions up
				* b (both) rounds fractions up or down [default]
			-ends: end pozition, SG(ends) = 0
	'''
	def __init__(self, denums, mode = "b", ends = 1):
		self.denums = denums
		self.mode = mode
		self.ends = ends
		print("Denumerators: " + str(self.denums) +
		"\nMode: " + str(self.mode) +
		"\nEnds: " + str(self.ends))
		if self.mode == "u":
			print("Rounding fractions up")
			self.getDep = getattr(mex, 'ceil')
		elif self.mode == "d":
			print("Rounding fractions down")
			self.getDep = getattr(mex, 'floor')
		else:
			print("Rounding fractions up and down")
			self.getDep = getattr(mex, 'both')
		
		
	def dependsOn(self, n):
		'''
			Calculates and returns possible moves from the given position (n) in the game.
		'''
		dependants = []
		for denum in self.denums:
			self.getDep(n, denum, dependants)
		return dependants
		
	def nimRow(self, n):
		'''	
			Calculates the NIM row up to b.
		'''
		self.nims = []
		for i in range(self.ends+1):
			self.nims.append(0)
			
		for i in range(n):
			deps = self.dependsOn(i+self.ends + 1)
#			print(str(i + self.ends + 1) + " atkarības")
#			print(deps)
#			print(self.nims)
			nim_deps = []
			for dep in deps:
				try:
					nim_deps.append(self.nims[dep])
				except IndexError:
					nim_deps.append(0)
#			print(nim_deps)
			self.nims.append(mex.mex(nim_deps))
			
	def plotNimRow(self, n, directory = ''):
		'''
			Displays the NIM row in a plot.
			If self.nims is empty calls self.nimRow()
			If value of directory is not set, uses ./plots/<self.mode>-<self.ends>/
		'''
		if len(directory) < 1:
			directory = './plots/' + str(self.mode) + '-' + str(self.ends) + '/'
		if not os.path.exists(directory):
			try:
				os.makedirs(directory)
			except Exception as e:
				print("Error: " + str(e))

		filename = directory + 'plt-d' + str(self.denums).replace('[','').replace(']','').replace(' ','').replace(',',':') + str(self.mode) + str(self.ends) + '-n=' + str(n) + ''
		
		if len(self.nims) < 1:
			self.nimRow(n)
		plt.clf()
		plt.step(range(len(self.nims)), self.nims, 'g', linewidth=4, where='post', fillstyle='full')
		plt.xscale('log')
		plt.ylim(0, max(self.nims) + 0.5)
		plt.xlabel('$n$')
		plt.ylabel('$SG(n)$')
		plt.savefig(filename + '.ps')
		os.system('ps2pdfwr ' + filename + '.ps ' + filename + '.pdf')
		os.system('rm ' + filename + '.ps')
		os.system('pdfcrop ' + filename + '.pdf ' + filename + '.pdf')
		os.system('nohup evince ' + filename + '.pdf > /dev/null &')
		
	def saveNimRow(self, n, struct = "key", directory = ''):
		'''
			Saves NIM row in a file
			If mode == all, saves full row
			If mode == key (defaults) saves only the positions where NIM value changes
			If self.nims is empty calls self.nimRow()
			If value of directory is not set, uses ./data/<self.mode>-<self.ends>/
		'''
		if struct != "all" and struct != "key":
			print("Invalid struct at saveNimRow(), allowed 'all' vai 'key'")
			raise Exception('saveNimRow: struct (', mode, ')')

		if len(directory) < 1:
			directory = './data/' + str(self.mode) + '-' + str(self.ends) + '/'
		if not os.path.exists(directory):
			try:
				os.makedirs(directory)
			except Exception as e:
				print("Error: " + str(e))

		filename = directory + 'data-d' + str(self.denums).replace('[','').replace(']','').replace(' ','').replace(',',':') + str(self.mode) + str(self.ends) + '-n=' + str(n) + '.dat'
		
		if len(self.nims) < 1:
			self.nimRow(n)

		ptr = open(filename, 'w')
		prevNim = None
		lines = 0
		for i in range(n+1):
			if struct == "key" and prevNim != self.nims[i]:
				ptr.write(str(i) + " " + str(self.nims[i]) + "\n")
				lines += 1
			elif struct == "all":
				ptr.write(str(i) + " " + str(self.nims[i]) + "\n")
				lines += 1
			prevNim = self.nims[i]
		ptr.close()
		print(str(lines) + " lines with NIM values written to " + filename)
	
	def saveTexRow(self, n, directory = ''):
		'''
			Saves NIM row in a TeX format
			If self.nims is empty calls self.nimRow()
			If value of directory is not set, uses ./data/<self.mode>-<self.ends>/
		'''
		if len(directory) < 1:
			directory = './tex/' + str(self.mode) + '-' + str(self.ends) + '/'
		if not os.path.exists(directory):
			try:
				os.makedirs(directory)
			except Exception as e:
				print("Error: " + str(e))

		filename = directory + 'tex-d' + str(self.denums).replace('[','').replace(']','').replace(' ','').replace(',',':') + str(self.mode) + str(self.ends) + '-n=' + str(n) + '.tex'
		
		if len(self.nims) < 1:
			self.nimRow(n)

		prevNim = None
		lines = 0
		pos = ['$n$']
		vals = ['$SG(n)$']
		defs = ['r']
		for i in range(n+1):
			#ptr.write(str(i) + " " + str(self.nims[i]) + "\n")
			if prevNim != self.nims[i]:
				pos.append(str(i))
				vals.append(str(self.nims[i]))
				defs.append('c')
				lines += 1
			prevNim = self.nims[i]
		ptr = open(filename, 'w')
		ptr.write("\\begin{tabular}{" + "|".join(defs) + "}" + "\n")
		ptr.write("\t" + " & ".join(pos) + "\\\\\\hline\n")
		ptr.write("\t" + " & ".join(vals) + "\n")
		ptr.write("\\end{tabular}")
		ptr.close()
		print(str(lines) + " cols with NIM values written to " + filename)

