# -*- coding: utf-8 -*-

from math import ceil as mceil
#from math import floor as mfloor

def mex(vals): # aprēķina mex() vērtību, vals ir masīvs ar argumentiem
	'''
		Calculates the Minimal EXclusive (MEX) value of the given Python list.
		Examples:
		>>> mex([0,1,2])
		>>> 3
		>>> mex([1,2,4])
		>>> 0
	'''
	i = 0
	while i < len(vals):
		if i not in vals:
			break;
		i += 1
	return i
	
def ceil(num, denum, row):
	'''
		Calculates quotient by rounding up and appends it to the list if the value is not present in the list.
	'''
#	result = num//denum + bool(num%denum)
	result = mceil(num/denum)
	if result not in row:
		row.append(result)

def floor(num, denum, row):
	'''
		Calculates quotient by rounding down and appends it to the list if the value is not present in the list.
	'''
	result = num//denum
#	result = mfloor(num/denum)
	if result not in row:
		row.append(result)

def both(num, denum, row):
	'''
		Calculates quotients by rounding up and down and appends they to the list if the values are not present in the list.
	'''
#	result = num//denum + bool(num%denum)
	result = mceil(num/denum)
	if result not in row:
		row.append(result)
	result = num//denum
#	result = mfloor(num/denum)
	if result not in row:
		row.append(result)

