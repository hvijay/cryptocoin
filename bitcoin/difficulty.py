#!/usr/bin/env python

'''
this script calculates the difficulty of bitcoin as a 
number given the compact target in hex
e.g., http://blockexplorer.com/b/330231
'''

EXPONENT_MASK = 0x1f000000 # lower 5 bits of top byte
EXPONENT_SHIFT = 24 # to get the top byte
CORRECTION = 3
MANTISSA_MASK = 0xffffff # lower 3 bytes
BASE = 256
MAX_TARGET = 0x1d00ffff # maximum target value (for easiest difficulty = 1)

def target(compact_target):
	''' 
	target is the number a valid hash has to be below. 
	smaller the target, more difficult to solve. 
	'''
	ct = int(compact_target, 16) # integer representation
	exponent = ((ct & EXPONENT_MASK) >> EXPONENT_SHIFT) - CORRECTION
	mantissa = (ct & MANTISSA_MASK)
	base = BASE
	difficulty = mantissa * (base ** (exponent))
	return difficulty

def difficulty(compact_target):
	tgt = target(compact_target) 
	max_tgt = target('1d00ffff')
	return max_tgt / tgt

	
print difficulty('181bc330')
