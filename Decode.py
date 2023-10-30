# Imports
import heapq
import string
from encode import Node, chars, build_huffman_tree, generate_huffman_codes

# Reconstruct tree from frequencies
def read_freqs(fname):
    freqs = {}
    with open(fname) as f:
        for line in f:
            char, freq = line.split(':')
            freqs[char] = int(freq)
    return freqs

tree = build_huffman_tree(read_freqs('frequency.txt'))

#print (tree)

# Read codewords 
def read_codes(fname):
    codes = {}
    with open(fname) as f:
        for line in f:
            char, code = line.split(':')
            codes[char] = code
    return codes

codes = read_codes('codes.txt')

#check if the codes are correct
#print(codes)

whitespace = chr(32) + chr(9) + chr(10) + chr(13)

# Decode compressed data
def decode(infile, outfile):
    with open(infile, 'rb') as f_in:
        bindata = f_in.read()
  
    bits = ''
    for byte in bindata:
        bits += '{0:08b}'.format(byte) 

    text = '' 
    node = tree
    for bit in bits:
        if bit == '1':
            node = node.left 
        else:
            node = node.right
            
        if node.char in chars:
            text += node.char
            node = tree
            
    with open(outfile, 'w') as f_out:
        f_out.write(text)
 
# Driver        
if __name__ == '__main__':
    decode('compressed.bin', 'decoded.txt')
