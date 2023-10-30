import heapq
from collections import Counter
import string
whitespace = set(string.whitespace)


from collections import OrderedDict

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    def __lt__(self, other):
        return self.freq < other.freq
    
    def __le__(self, other):
        return self.freq <= other.freq
    
    def __gt__(self, other):
        return self.freq > other.freq
    
    def __ge__(self, other):
        return self.freq >= other.freq

# List of all possible characters
chars = [' ', ',', '.'] + list(string.digits) + list(string.ascii_lowercase)

# Initialize frequencies with 0 for all chars
frequencies = {char:0 for char in chars}

with open('test1.txt') as f:
    for line in f:
        line = line.lower()  

        for char in line:

            if char.isspace():
                char = ' '
            char = char.lower()

            if char.isalnum() or char in ' ,.':
                frequencies[char] += 1
                


def build_huffman_tree(freq_dict):
    priority_queue = [Node(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left_node = heapq.heappop(priority_queue)
        right_node = heapq.heappop(priority_queue)
        new_node = Node(None, left_node.freq + right_node.freq)
        new_node.left = left_node
        new_node.right = right_node
        heapq.heappush(priority_queue, new_node)

    return priority_queue[0]

# Generating Huffman Codes
def generate_huffman_codes(node, current_code, huffman_codes):
    if node.char:
        huffman_codes[node.char] = current_code
    else:
        generate_huffman_codes(node.left, current_code + '1', huffman_codes)
        generate_huffman_codes(node.right, current_code + '0', huffman_codes)

huffman_tree = build_huffman_tree(frequencies)

'''tree visualizer
def print_huffman_tree(node, level=0):
    if node:
        indent = '    ' * level
        print(indent + f'{node.char}: {node.freq}')
        print_huffman_tree(node.left, level + 1)
        print_huffman_tree(node.right, level + 1)

print("Huffman Tree:")
print_huffman_tree(huffman_tree)
'''
huffman_codes = {}
generate_huffman_codes(huffman_tree, '', huffman_codes)

for char in huffman_codes:
    if char in whitespace:
        huffman_codes[char] = huffman_codes[' ']

sorted_codes = sorted(huffman_codes.items(), key=lambda item: len(item[1]))


# Writing Huff_Codes to File
with open('codes.txt', 'w') as file:
    for char, code in sorted_codes:
        file.write(f"{char}: {code}\n")

with open('frequency.txt', 'w') as f:
    for char, freq in frequencies.items():
        f.write(f'{char}:{freq}\n')


# Compress file
with open('test1.txt') as f, open('compressed.bin', 'wb') as out:

  bitstring = 0
  bits = 0
  
  for line in f:
    line = line.lower()
    
    for char in line:
    
      if char in huffman_codes:
      
        code = huffman_codes[char]
      
        for bit in code:
        
          bit = 0 if bit == '0' else 1
        
          bitstring = (bitstring << 1) | bit 
          bits += 1
          
          if bits == 8:
            out.write(bitstring.to_bytes(1, 'big'))
            bitstring = 0
            bits = 0

  if bits > 0:
    bitstring <<= (8 - bits)
    out.write(bitstring.to_bytes(1, 'big'))