class VigenereCipher:
    def __init__(self):
        pass

    def vigenere_encrypt(self, plain_text, key):
        if not key or not any(c.isalpha() for c in key):
            return plain_text
            
        encrypted_text = ""
        key_index = 0
        clean_key = [c.upper() for c in key if c.isalpha()]
        
        for char in plain_text:
            if char.isalpha():
                key_shift = ord(clean_key[key_index % len(clean_key)]) - ord('A')
                if char.isupper():
                    encrypted_text += chr((ord(char) - ord('A') + key_shift) % 26 + ord('A'))
                else:
                    encrypted_text += chr((ord(char) - ord('a') + key_shift) % 26 + ord('a'))
                key_index += 1
            else:
                encrypted_text += char
        return encrypted_text

    def vigenere_decrypt(self, encrypted_text, key):
        if not key or not any(c.isalpha() for c in key):
            return encrypted_text
            
        decrypted_text = ""
        key_index = 0
        clean_key = [c.upper() for c in key if c.isalpha()]
        
        for char in encrypted_text:
            if char.isalpha():
                key_shift = ord(clean_key[key_index % len(clean_key)]) - ord('A')
                if char.isupper():
                    decrypted_text += chr((ord(char) - ord('A') - key_shift + 26) % 26 + ord('A'))
                else:
                    decrypted_text += chr((ord(char) - ord('a') - key_shift + 26) % 26 + ord('a'))
                key_index += 1
            else:
                decrypted_text += char
        return decrypted_text

    def encrypt_text(self, text, key):
        return self.vigenere_encrypt(text, key)

    def decrypt_text(self, text, key):
        return self.vigenere_decrypt(text, key)