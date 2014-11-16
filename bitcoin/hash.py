#!/usr/bin/env python
'''
this script shows how the bitcoin hash is 
calculated given a raw block (as a json file). 
e.g., http://blockexplorer.com/rawblock/00000000000000001e8d6829a8a21adc5d38d0a473b144b6765798e61f98bd1d
'''

import json
import hashlib
import binascii

def str_byte_rev(s):
	t = bytearray(len(s))
	t[1::2], t[::2] = s[::2], s[1::2]
	return str(t[::-1])

class BTCBlock:
	# version (4 bytes)
	# prev_block (32 bytes)
	# mrkl_root (32 bytes)
	# time (4 bytes)
	# bits (compact_target) (4 bytes)
	# nonce (solution) (4 bytes)
	size = [4, 32, 32, 4, 4, 4] # in bytes
	
	def __init__(self, json_file):
		h = json.load(open(json_file))
		self.ver = h["ver"]
		self.prev_block = h["prev_block"]
		self.mrkl_root = h["mrkl_root"]
		self.time = h["time"]
		self.bits = h["bits"]
		self.nonce = h["nonce"]
		self.vals = [self.ver, self.prev_block, self.mrkl_root, self.time, self.bits, self.nonce]


	def hash(self):
		''' 
		the hash of a block is calculated by:
			(1) converting each value in (1) to hex string if required (without 0x, with leading 0s to fill size)
			(2) reversing order of bytes for each string in (1)
			(3) concatenating each string in (3) in the order of fields above
			(4) converting string in (3) to int
			(5) taking sha256(sha256((4))) 
		'''
		# (1) 
		# convert to hex string
		hex_vals = [hex(v)[2:] if type(v) is int else str(v) for v in self.vals]

		# fill with leading 0s (2 '0's for each byte)
		hex_vals = [v.zfill(self.size[i] * 2) for (i, v) in enumerate(hex_vals)]

		# (2) : reverse order of bytes for each value 
		rev_hex_vals = []
		for s in hex_vals:
			rev_hex_vals.append(str_byte_rev(s))

		# (3) : concatenate 
		str_to_hash = ''.join(rev_hex_vals)
		
		# (4) : convert string to int
		int_to_hash = binascii.a2b_hex(str_to_hash)

		# (5) : take sha256(sha256)
		hsh = binascii.b2a_hex(hashlib.sha256(hashlib.sha256(int_to_hash).digest()).digest())

		return str_byte_rev(hsh)

b = BTCBlock('125552.block')
print 'hash: {0}'.format(b.hash())
