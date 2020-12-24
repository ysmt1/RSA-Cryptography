import binascii

from RSAAlgorithm import RSAAlgorithm
from Utilities import debug_stream

class RSACodec:
    '''
    Wrapper class around RSAAlgorithm class. Reads data from an
    input stream, encrypts or decrypts the data, and writes results to an output stream.
    '''
    def __init__(self, p, q, e):
        self.p = p
        self.q = q
        self.e = e
        self.RSAAlgorithm_ = RSAAlgorithm(self.p, self.q, self.e)

    # getters
    @property
    def n(self):
        return self.RSAAlgorithm_.n

    @property
    def max_length(self):
        return self.__calculate_block_max_length(self.n) 

    # private methods
    def __calculate_block_max_length(self, n):
        '''
        Calculate max block length
        '''
        m = 0
        max_length = -1
        while m < n:
            m = m << 8 | 0xff
            max_length += 1
        return max_length

    def __divide_to_blocks(self, string, length):
        '''
        Divide data into blocks for processing
        '''
        return (string[0 + i: length + i] for i in range(0, len(string), length))

    def encrypt_stream(self, fin, fout):
        '''
        Reads unencrypted data from a given binary input stream, encrypts the data,
        and writes the encrypted results to a given text output stream.
        '''
        from Utilities import debug_stream

        file_content = fin.read()
        encrypted_fstream = open(fout, 'w')

        blocks = list(self.__divide_to_blocks(file_content, self.max_length))
        self.encrypted_blocks = []

        for i, block in enumerate(blocks):
            hex_rep = block.hex()
            M = int(hex_rep, 16)
            C = self.RSAAlgorithm_.encrypt(M)
            self.encrypted_blocks.append(C)

            print(f'\n--- RSACodec::encryptStream block #{i}, max length {self.max_length} ---\n', file=debug_stream)
            print(f'Requested count {len(block)} bytes, got', file=debug_stream)
            for i, c in enumerate(block):
                print(f'[{i}]',repr(chr(c)), end=" ", file=debug_stream)
            print('\n', file=debug_stream)
            print(f'Read {"0x" + format(M, "X")} as {len(block)} bytes \n', file=debug_stream)
            print(f'RSAAlgorithm::encrypt {"0x" + format(M, "X")} -> {"0x" + format(C, "X")}\n', file=debug_stream)

            print(format(len(block), 'X'), format(C, 'X'), file=encrypted_fstream)

        encrypted_fstream.close()

    def decrypt_stream(self, fout):
        '''
        Reads encrypted data from a given text input stream, decrypts the data, and
        writes the decrypted results to a given binary output stream.
        '''
        from Utilities import debug_stream

        decrypted_fstream = open(fout, 'wb')

        for i, block in enumerate(self.encrypted_blocks):
            M_prime = self.RSAAlgorithm_.decrypt(block)
            hex_s = format(M_prime, "x")
            if len(hex_s) % 2 != 0:
                hex_s = '0' + hex_s
            binary_s = binascii.unhexlify(hex_s)

            print(f'\n--- RSACodec::decryptStream block #{i}, length {len(binary_s)} ---\n', file=debug_stream)
            print(f'RSAAlgorithm::decrypt {"0x" + format(block, "X")} -> {"0x" + format(M_prime, "X")}\n', file=debug_stream)
            print(f'Writing {"0x" + format(M_prime, "X")} as {len(binary_s)} bytes \n', file=debug_stream)

            for i_, c in enumerate(binary_s):
                print(f'[{i_}]',repr(chr(c)), end=" ", file=debug_stream)

            print('\n', file=debug_stream)

            decrypted_fstream.write(binary_s)

        decrypted_fstream.close()

