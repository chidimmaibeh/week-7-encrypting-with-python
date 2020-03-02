from cryptography.fernet import Fernet


class Cipher:

    def __init__(self, key):
        self.key = key

    # This method is used for general encryption
    def encrypt(self, plaintext):
        data = plaintext.encode('utf-8')
        crypter = Fernet(self.key)
        encrypted = crypter.encrypt(data)
        return encrypted

    # This method is used for general decryption
    def decrypt(self, encrytedtext):
        f = Fernet(self.key)
        decrypted = f.decrypt(encrytedtext.encode())
        return decrypted
