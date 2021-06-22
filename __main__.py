from bmp_file import BmpFile
from built_in_rsa import BuiltInRsa
from electronic_codebook import ElectronicCodebook
from own_rsa import OwnRsa


if __name__ == '__main__':
    # BLOCK_SIZE = 25
    # original_bmp_file = BmpFile('tux.bmp')
    # original_bmp_file = BmpFile('rgb24lprof.bmp')
    # original_bmp_file = BmpFile('LAND3.bmp')

    # built_in_rsa = BuiltInRsa()
    # key_pair = built_in_rsa.generate_key(BLOCK_SIZE * 8 + 1)
    #
    # electronic_codebook = ElectronicCodebook(OwnRsa(), BLOCK_SIZE, key_pair)
    # original_bmp_file.save_encrypted_file(electronic_codebook, "encrypted_file_own_rsa.bmp")
    # bmp_file = BmpFile('encrypted_file_own_rsa.bmp')
    # bmp_file.save_decrypted_file(electronic_codebook, "decrypted_file_own_rsa.bmp")
    #
    # electronic_codebook2 = ElectronicCodebook(BuiltInRsa(), BLOCK_SIZE, key_pair)
    # original_bmp_file.save_encrypted_file(electronic_codebook2, "encrypted_file_built_in_rsa.bmp")
    # bmp_file = BmpFile('encrypted_file_built_in_rsa.bmp')
    # bmp_file.save_decrypted_file(electronic_codebook2, "decrypted_file_built_in_rsa.bmp")
