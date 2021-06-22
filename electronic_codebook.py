import math

from rsa_algorithm import RsaAlgorithm

BITS_IN_BYTE = 8


class ElectronicCodebook:
    def __init__(self, algorithm: RsaAlgorithm, block_length_in_bytes: int):
        self.algorithm = algorithm
        self.public_key, self._private_key = self.algorithm.generate_key(block_length_in_bytes * BITS_IN_BYTE + 1)
        self.block_length_in_bytes = block_length_in_bytes
        self.encrypted_block_length_in_bytes = self._round_up_to_bytes(self.public_key.n.bit_length())

    def encrypt(self, byte_array):
        encrypted_blocks = []
        for block in self._split_byte_array_into_blocks(byte_array, self.block_length_in_bytes):
            encrypted_block = self.algorithm.encrypt(self.public_key, block)
            encrypted_block_with_leading_zeros = self._fill_byte_array_with_leading_zeros(
                encrypted_block, self.encrypted_block_length_in_bytes)
            encrypted_blocks.append(encrypted_block_with_leading_zeros)
        return b''.join(encrypted_blocks)

    def decrypt(self, byte_array):
        decrypted_blocks = []
        encrypted_blocks = self._split_byte_array_into_blocks(byte_array, self.encrypted_block_length_in_bytes)
        for index, block in enumerate(encrypted_blocks):
            decrypted_block = self.algorithm.decrypt(self._private_key, block)
            if index < len(encrypted_blocks) - 1:
                decrypted_blocks.append(self._fill_byte_array_with_leading_zeros(
                    decrypted_block, self.block_length_in_bytes))
            else:
                decrypted_blocks.append(decrypted_block)
        return b''.join(decrypted_blocks)

    def _split_byte_array_into_blocks(self, byte_array, block_size):
        return [byte_array[i:(i + block_size)] for i in range(0, len(byte_array), block_size)]

    def _round_up_to_bytes(self, number_of_bits):
        return math.ceil(number_of_bits / 8)

    def _fill_byte_array_with_leading_zeros(self, byte_array, size):
        return bytearray.fromhex("00") * (size - len(byte_array)) + byte_array
