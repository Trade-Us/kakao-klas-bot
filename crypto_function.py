from cryptography.fernet import Fernet 

class SymmetricKeyAgent:
    def __init__(self):
        self._key = self._load_key()
        self._cipher_suite = Fernet(self._key)
    def _load_key(self):
        """
        Loads the key from the current directory named `key.key`
        """
        return open("./keystore/key.key", "rb").read()

    def encrypt(self, password):
        data = self._cipher_suite.encrypt(password.encode('utf-8'))
        return data.decode('utf-8')

    def decrypt(self, data):
        password = self._cipher_suite.decrypt(data.encode('utf-8'))
        return password.decode('utf-8')

