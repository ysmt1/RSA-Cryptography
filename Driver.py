import os

import Utilities
from RSAAlgorithm import RSAAlgorithm
from RSACodec import RSACodec

def test_encrypting(key_file, input_file, debug_file, encrypted_file):
    '''
    Begin encryption process of input file.  Writes encrypted data to encrypted file output
    '''
    global rsa_codec
    
    keys = Utilities.get_vars(key_file)
    p, q, e = keys['p'], keys['q'], keys['e']

    Utilities.debug_stream = open(debug_file, 'w')
    print(f'*** Testing file {input_file}, debug output file {debug_file} ***\n')

    rsa_codec = RSACodec(p, q, e)

    Utilities.debug_stream.write(f'\n*** Encrypting {input_file}, size {os.path.getsize(input_file)} -> {encrypted_file} ***\n')

    input_stream = open(input_file, 'rb')
    rsa_codec.encrypt_stream(input_stream, encrypted_file)

    Utilities.debug_stream.write(f'Encrypted file {encrypted_file} size is {os.path.getsize(encrypted_file)}\n')

def test_decrypting(encrypted_file, decrypted_file):
    '''
    Begin decryption process of encrypted file.  Writes decrypted data to decrypted file output
    '''

    Utilities.debug_stream.write(f'\n*** Decrypting {encrypted_file}, size {os.path.getsize(encrypted_file)} -> {decrypted_file} ***\n')

    rsa_codec.decrypt_stream(decrypted_file)

    Utilities.debug_stream.write(f'Decrypted file {decrypted_file} size is {os.path.getsize(decrypted_file)}\n')

def main():
    '''
    Main driver function to encrypt given .dat file and test encryption
    Need a keymat file which provides p, q, and e variables
    '''

    input_files, key_files = Utilities.read_files()

    for index, input_file in enumerate(input_files):
        key_file = key_files[index]
        debug_file = key_file.replace('keymat', 'debug')
        encrypted_file = key_file.replace('keymat', 'encrypted')
        decrypted_file = input_file.replace('in', 'decrypted')

        test_encrypting(key_file, input_file, debug_file, encrypted_file)
        test_decrypting(encrypted_file, decrypted_file)

        Utilities.compare_files(input_file, decrypted_file)

        Utilities.debug_stream.write(f"\n!!! Files {input_file} and {decrypted_file} are equal.")
        Utilities.debug_stream.close()
        
        print("\nOK\n\n")

if __name__ == '__main__':
    main()