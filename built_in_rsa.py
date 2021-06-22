from rsa_algorithm import RsaAlgorithm
import rsa


class BuiltInRsa(RsaAlgorithm):

    def generate_key(self, n_bit_range):
        pubkey, privkey = rsa.newkeys(n_bit_range + 128)
        while (pubkey.n.bit_length() - 12) < (n_bit_range // 8):
            pubkey, privkey = rsa.newkeys(n_bit_range + 30)
        return pubkey, privkey

    def encrypt(self, public_key, plain_text):
        return rsa.encrypt(plain_text, public_key)

    def decrypt(self, private_key, ciphertext):
        return rsa.decrypt(ciphertext, private_key)

