#!/usr/bin/env python
'''
this script shows how the bitcoin hash is 
calculated given a raw block (as a json file). 
e.g., http://blockexplorer.com/rawblock/00000000000000001e8d6829a8a21adc5d38d0a473b144b6765798e61f98bd1d
'''

import json
import hashlib
import binascii

def swap_byte_order(s):
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
		self.tx_hashes = [t["hash"] for t in h["tx"]]
		self.vals = [self.ver, self.prev_block, self.mrkl_root, self.time, self.bits, self.nonce]


	def mrkl_hash(self):
		'''
		the root hash of the merkle tree is calculated by:
			(1) duplicating last transaction if odd number of transactions
			(2) reversing bytes
			(3) calculating parent hash = concatenated hash of pairs 
			(4) recursively calculating (1) - (3) until we are left with root
		reference: https://en.bitcoin.it/wiki/Protocol_specification#Merkle_Trees
		'''
		children = list(self.tx_hashes)
		children = [str(c) for c in children]
		while len(children) != 1:
			parents = []
			if len(children) % 2 != 0:
				children.append(children[-1])
			children = [swap_byte_order(c) for c in children]
			for i in range(0, len(children), 2):
				c = children[i] + children[i+1]
				parents.append(self.coin_hash(c))
			children = parents

		return children[0]

	def coin_hash(self, s):
		'''
		@s: string to hash
		'''
		# (4) : convert string to int
		int_to_hash = binascii.a2b_hex(s)

		# (5) : take sha256(sha256)
		hsh = binascii.b2a_hex(hashlib.sha256(hashlib.sha256(int_to_hash).digest()).digest())

		return swap_byte_order(hsh)
		
	def block_hash(self):
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
			rev_hex_vals.append(swap_byte_order(s))

		# (3) : concatenate 
		str_to_hash = ''.join(rev_hex_vals)
		
		# (4) : convert string to int
		int_to_hash = binascii.a2b_hex(str_to_hash)

		# (5) : take sha256(sha256)
		hsh = binascii.b2a_hex(hashlib.sha256(hashlib.sha256(int_to_hash).digest()).digest())

		return swap_byte_order(hsh)

b = BTCBlock('125552.block')
print 'mrkl root hash: {0}'.format(b.mrkl_hash())
print 'block hash: {0}'.format(b.block_hash())
