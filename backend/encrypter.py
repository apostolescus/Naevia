import re
from collections import OrderedDict
import string


class Encrypter:
    @staticmethod
    def preprocess_plaintext(plaintext):
        return re.sub("[^a-zA-Z]+", "", plaintext.upper())

    @staticmethod
    def caesar_encrypt(plaintext, key):
        plaintext = Encrypter.preprocess_plaintext(plaintext)

        cipher = ""
        for i in range(len(plaintext)):
            letter = plaintext[i]
            cipher += chr((ord(letter) + key - 65) % 26 + 65)

        return cipher

    @staticmethod
    def generate_vigenere_key(plaintext, key):
        key = list(key.upper())

        if len(plaintext) == len(key):
            return (key)
        else:
            for i in range(len(plaintext) - len(key)):
                key.append(key[i % len(key)])

        return "".join(key)

    @staticmethod
    def vigenere_encrypt(plaintext, key, is_encrypt=True):
        plaintext = Encrypter.preprocess_plaintext(plaintext)
        processed_key = Encrypter.generate_vigenere_key(plaintext, key)

        cipher = ""
        for i in range(len(plaintext)):
            index = 26 + ord(
                plaintext[i]) + pow(-1, 1 + is_encrypt) * ord(processed_key[i])
            cipher += chr(index % 26 + ord('A'))

        return cipher

    @staticmethod
    def generate_substition_key(key):
        key = key.upper()
        key = "".join(OrderedDict.fromkeys(key))

        for character in string.ascii_uppercase:
            if character not in key:
                key += character

        return key

    @staticmethod
    def substitution_encrypt(plaintext, key):
        plaintext = Encrypter.preprocess_plaintext(plaintext)
        key = Encrypter.generate_substition_key(key)

        cipher = ""
        for character in plaintext:
            index = string.ascii_uppercase.find(character)
            cipher += key[index]

        return cipher