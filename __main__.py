import math

import rsa

from sympy import randprime

from bmp_file import BmpFile
from built_in_rsa import BuiltInRsa
from electronic_codebook import ElectronicCodebook
from own_rsa import OwnRsa


def electronic_codebook(byte_array, size):
    return [byte_array[i:(i+size)] for i in range(0, len(byte_array), size)]


def RSA_using_built_in_library(byte_array):
    key_range = 512
    pubkey, privkey = rsa.newkeys(key_range)
    # print(pubkey, privkey)
    chunks = electronic_codebook(byte_array, key_range // 10)
    encrypted_chunks = []
    decrypted_chunks = []
    for chunk in chunks:
        encrypted_chunk = rsa.encrypt(chunk, pubkey)
        encrypted_chunks.append(encrypted_chunk)
        decrypted_chunks.append(rsa.decrypt(encrypted_chunk, privkey))

    encrypted_chunks_as_one = b''.join(encrypted_chunks)
    decrypted_chunks_as_one = b''.join(decrypted_chunks)

    encrypted_file = bmp_file.get_image_header() + encrypted_chunks_as_one + bmp_file.get_image_footer()
    with open("encrypted_file.bmp", "wb") as file:
        file.write(encrypted_file)

    decrypted_file = bmp_file.get_image_header() + decrypted_chunks_as_one + bmp_file.get_image_footer()
    with open("decrypted_file.bmp", "wb") as file:
        file.write(decrypted_file)


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def binary_little_endian_to_int(array):
    byte_sum = 0
    multiplier = 1
    for byte in array:
        byte_sum += byte * multiplier
        multiplier *= 2**8
    return byte_sum


def fast_modular_exponentiation(base, exponent, modulus):
    if exponent == 0:
        return 1
    if exponent == 1:
        return base % modulus
    if exponent % 2 == 0:
        result = fast_modular_exponentiation(base, exponent // 2, modulus)
        return (result * result) % modulus
    if exponent % 2 != 0:
        result = fast_modular_exponentiation(base, exponent // 2, modulus)
        return (((result * result) % modulus) * base) % modulus


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


def my_RSA(byte_array):
    p = 0
    q = 0
    while p == q:
        p = randprime(1024, 1060)
        q = randprime(1100, 1300)
        # print(p, q)
    n = p * q
    euler = (p - 1) * (q - 1)
    print(f"n= {n}")
    e = randprime(2, euler)
    while math.gcd(e, euler) != 1:
        e = randprime(2, euler)

    d = modinv(e, euler)
    # print(d)

    max_chunk_size = 1

    chunks = electronic_codebook(byte_array, max_chunk_size)

    encrypted_chunks = []
    decrypted_chunks = []
    for chunk in chunks:
        int_chunk = binary_little_endian_to_int(chunk)
        encrypted_chunk = pow(int_chunk, e, n)
        print(f"m= {int_chunk}")
        # print(encrypted_chunk)
        encrypted_chunks.append(encrypted_chunk)
        decrypted_chunks.append(pow(encrypted_chunk, d, n))

    encrypted_chunks_as_bytes = bytearray()

    for encrypted_chunk in encrypted_chunks:
        encrypted_chunks_as_bytes += int_to_bytes(encrypted_chunk)

    print(f"encrypted_chunks_as_bytes= {encrypted_chunks_as_bytes}")

    decrypted_chunks_as_bytes = bytearray()

    for decrypted_chunk in decrypted_chunks:
        decrypted_chunks_as_bytes += int_to_bytes(decrypted_chunk)

    print(f"decrypted_chunks_as_bytes= {decrypted_chunks_as_bytes}")

    encrypted_file = bmp_file.get_image_header() + encrypted_chunks_as_bytes + bmp_file.get_image_footer()
    with open("encrypted_file.bmp", "wb") as file:
        file.write(encrypted_file)

    decrypted_file = bmp_file.get_image_header() + decrypted_chunks_as_bytes + bmp_file.get_image_footer()
    with open("decrypted_file.bmp", "wb") as file:
        file.write(decrypted_file)


if __name__ == '__main__':
    # bmp_file = BmpFile('rgb24lprof.bmp')
    # bmp_file = BmpFile('tux.bmp')
    bmp_file = BmpFile('LAND3.bmp')
    # bmp_file.print_file_attributes()
    print()
    electronic_codebook = ElectronicCodebook(OwnRsa(), 25)
    # electronic_codebook = ElectronicCodebook(BuiltInRsa(), 10)
    bmp_file.save_encrypted_file(electronic_codebook)

    bmp_file = BmpFile('encrypted_file.bmp')
    bmp_file.print_file_attributes()
    print()
    bmp_file.save_decrypted_file(electronic_codebook)

    bmp_file = BmpFile('decrypted_file.bmp')
    bmp_file.print_file_attributes()
    print()


    # byte_array = bmp_file.get_image_data()
    # print(byte_array)
    # RSA_using_built_in_library(byte_array)
    # print("original image: ")
    # print(bmp_file.get_image_data())
    # my_RSA(byte_array)

    # print(([123]).to_bytes(5, byteorder='little'))

    # print(bytes([23443432345432345]))

    # print(fast_modular_exponentiation(2, 8, 5))

    # print(([5]).to_bytes(5, byteorder='little'))

    # number_to_cipher = b'2131212413'
    # print(number_to_cipher)
    # electronic_codebook = ElectronicCodebook(OwnRsa(), 5)
    # encrypted = electronic_codebook.encrypt(number_to_cipher)
    # decrypted = electronic_codebook.decrypt(encrypted)
    # print(encrypted, decrypted)

    # rsa = OwnRsa()
    # brsa = BuiltInRsa()
    # pubkey, privkey = rsa.generate_key(256)
    # encrypted = rsa.encrypt(pubkey, number_to_cipher)
    # decrypted = rsa.decrypt(privkey, encrypted)
    # print(pubkey,privkey)
    # print(encrypted, decrypted)

    # encrypted = brsa.encrypt(pubkey, number_to_cipher)
    # decrypted = brsa.decrypt(privkey, encrypted)
    # print(pubkey,privkey)
    # print(encrypted, decrypted)