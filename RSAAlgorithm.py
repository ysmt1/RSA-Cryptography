class RSAAlgorithm:
    '''
    Makes RSA keys and encrypts/decrypts data via RSA
    algorithm. Constructor takes three big numbers p, q, e
    '''

    def __init__(self, p, q, e):
        self.p = p
        self.q = q
        self.e = e

        self.__init_debug_stream()

    # getters
    @property
    def n(self):
        return self.p * self.q

    @property
    def phi(self):
        return (self.p - 1) * (self.q - 1)

    @property
    def d(self):
        return self.__calculate_modular_inverse(self.e, self.phi)

    # private methods
    def __init_debug_stream(self):
        '''Initialize output in debug file stream'''

        from Utilities import debug_stream
        debug_stream.write('--- RSA Algorithm \n')
        debug_stream.write(f'p {self.p} \n')
        debug_stream.write(f'q {self.q} \n')
        debug_stream.write(f'e {self.e} \n')
        debug_stream.write(f'n {self.n} \n')
        debug_stream.write(f'd {self.d} \n')
        debug_stream.flush()

    def __calculate_modular_inverse(self, a, m): 
        '''
        The two functions below are used to calculate the modular inverse
        Implemented from https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
        '''
        def egcd(a, b):
            if a == 0:
                return (b, 0, 1)
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)

        # application of Extended Euclidean Algorithm to find a modular inverse
        def modinv(a, m):
            g, x, y = egcd(a, m)
            if g != 1:
                raise Exception('modular inverse does not exist')
            return x % m

        return modinv(a, m)

    def encrypt(self, M):
        '''Calculate cipertext number'''

        C = pow(M, self.e, self.n)
        return C

    def decrypt(self, C):
        '''Calculate plaintext number'''

        M = pow(C, self.d, self.n)
        return M

