# encrypt.py
class Encryptor:
    def __init__(self, key_path):
        try:
            with open(key_path, 'r') as key_file:
                self.key = key_file.read().strip()
        except IOError:
            print("Unable to open key.txt. Please ensure the file exists and is accessible.")
            raise RuntimeError("Unable to open key file")

    def encrypt(self, input_text):
        return self.xor_encrypt_decrypt(input_text)

    def decrypt(self, encrypted_text):
        return self.xor_encrypt_decrypt(encrypted_text)

    def xor_encrypt_decrypt(self, input_text):
        output = []
        for i in range(len(input_text)):
            output_char = chr(ord(input_text[i]) ^ ord(self.key[i % len(self.key)]))
            output.append(output_char)
        return ''.join(output)