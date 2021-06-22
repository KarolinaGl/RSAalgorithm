import abc


class RsaAlgorithm(abc.ABC):
    @abc.abstractmethod
    def generate_key(self, n_bit_range):
        pass

    @abc.abstractmethod
    def encrypt(self, public_key, plain_text):
        pass

    @abc.abstractmethod
    def decrypt(self, private_key, ciphertext):
        pass
