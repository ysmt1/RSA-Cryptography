import glob
import os
import sys
import re

# global var attached to file debug stream to use across files
debug_stream = None

def read_files():
    '''
    Read input files and return arrays of file names
    '''
    input_files = glob.glob("*_in.dat")
    key_files = glob.glob("*_keymat.txt")
    return input_files, key_files

def compare_files(infile, decrypted_file):
    '''
    Compare input file and final decrypted file for equality - in size and contents
    '''
    
    # Check for file size
    if os.path.getsize(infile) != os.path.getsize(decrypted_file):
        raise RuntimeError('File sizes are not equal')
    
    with open(infile, 'rb') as f1:
        infile_content = f1.read()

    with open(decrypted_file, 'rb') as f2:
        decrypted_content = f2.read()
    
    # Check if files have the same content
    for byte_i, byte_d in zip(infile_content, decrypted_content):
        if byte_i != byte_d:
            raise RuntimeError("File contents are not the same")

def get_vars(file):
    '''
    Parse keymat file for vars q, p and e
    '''
    
    file_s = open(file, 'r')
    content = file_s.read()
    
    q_match = re.search('q\s[0-9]+', content).group(0)
    p_match = re.search('p\s[0-9]+', content).group(0)
    e_match = re.search('e\s[0-9]+', content).group(0)
    
    keys = {
        'q': int(q_match.split(" ")[1]),
        'p': int(p_match.split(" ")[1]),
        'e': int(e_match.split(" ")[1]),
    }
    return keys