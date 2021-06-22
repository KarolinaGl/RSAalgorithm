import math
import os
from collections import namedtuple

import sympy

from rsa_algorithm import RsaAlgorithm

from utilities import int_from_bytes, modinv, int_to_bytes

BITS_IN_BYTE = 8

PublicKey = namedtuple('PublicKey', ['n', 'e'])
PrivateKey = namedtuple('PrivateKey', ['n', 'e', 'd', 'p', 'q'])


def bytes2int(raw_bytes: bytes) -> int:
    return int.from_bytes(raw_bytes, 'big', signed=False)


def int2bytes(number: int) -> bytes:
    bytes_required = max(1, math.ceil(number.bit_length() / BITS_IN_BYTE))
    return number.to_bytes(bytes_required, 'big')


class OwnRsa(RsaAlgorithm):
    def generate_key(self, n_bit_range):
        p, q = self._generate_p_q(n_bit_range)
        n = p * q
        euler = (p - 1) * (q - 1)
        e = self._random_coprime((euler.bit_length() - 1) // BITS_IN_BYTE, euler)
        d = modinv(e, euler)
        public_key = PublicKey(n, e)
        private_key = PrivateKey(n, e, d, p, q)
        return public_key, private_key

    def encrypt(self, public_key, plain_text):
        return int2bytes(pow(bytes2int(plain_text), public_key.e, public_key.n))

    def decrypt(self, private_key, ciphertext):
        return int2bytes(pow(bytes2int(ciphertext), private_key.d, private_key.n))

    def _random_prime(self, byte_length):
        random_number = int_from_bytes(os.urandom(byte_length))
        while not sympy.isprime(random_number):
            random_number = int_from_bytes(os.urandom(byte_length))
        return random_number

    def _generate_p_q(self, n_bit_range):
        p_q_max_byte_length = (n_bit_range // 2 // BITS_IN_BYTE + 1)
        p = self._random_prime(p_q_max_byte_length)
        q = self._random_prime(p_q_max_byte_length)
        while abs(p - q) < 100 or (p * q).bit_length() < n_bit_range:
            print(p.bit_length(), q.bit_length(), (p * q).bit_length())
            p = self._random_prime(p_q_max_byte_length)
            q = self._random_prime(p_q_max_byte_length)
        return p, q

    def _random_coprime(self, byte_length, other_number):
        random_number = int_from_bytes(os.urandom(byte_length))
        while not self._is_coprime(random_number, other_number):
            random_number = int_from_bytes(os.urandom(byte_length))
        return random_number

    def _is_coprime(self, a, b):
        return math.gcd(a, b) == 1
