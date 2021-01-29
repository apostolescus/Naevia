import sys
import random
from encrypter import Encrypter
import keygen
import ngram

MAX_ITERATIONS = 3500
QUADGRAMS_FILE = "../data/quadgrams.txt"
MAX_VIGENERE_KEY_LENGTH = 12


class Decrypter:
    def __init__(self, cypher_text):
        self.cypher_text = Encrypter.preprocess_plaintext(cypher_text.upper())
        self.keygen = keygen.KeyGen()
        self.fitness = ngram.Heuristic(QUADGRAMS_FILE)
        self.best_score = -sys.maxsize - 1
        self.key = ""
        self.decrypted = ""
        self.intermediate_list = []

    def hillclimbing_decrypt(self, algorithm="substitution", boost=False):
        check = False
        key = ""

        # Generate the start key
        if algorithm == "vigenere":
            key = self.keygen.get_initial_key("vigenere",
                                              MAX_VIGENERE_KEY_LENGTH)
        else:
            key = self.keygen.get_initial_key("substitution")

        while check is False:
            check = True

            # Generate neighbor keys
            if algorithm == "vigenere":
                generated_keys = self.keygen.get_neighbours_vigenere(
                    key, boost)
            else:
                generated_keys = self.keygen.get_neighbours_substitution(
                    key, 300, 3)

            for k in generated_keys:
                # Try to decrypt the ciphertext
                if algorithm == "vigenere":
                    decrypted_text = Encrypter.vigenere_encrypt(
                        self.cypher_text, k, False)
                else:
                    decrypted_text = Encrypter.substitution_encrypt(
                        self.cypher_text, k)

                # Compute and check the heuristic of the generated ciphertext
                score = self.fitness.score(decrypted_text)
                if score > self.best_score:
                    self.best_score = score
                    self.key = k
                    self.decrypted = decrypted_text
                    self.intermediate_list.append(score)
                    key = k
                    check = False

        # Save the best key and try to decrypt using Vigenere
        if (algorithm == "substitution"):

            substitution_best_key = self.key
            substitution_best_score = self.best_score
            substitution_best_decrypted = self.decrypted
            substitution_best_intermediate_list = self.intermediate_list.copy()

            self.intermediate_list.clear()
            self.best_score = -sys.maxsize - 1

            self.hillclimbing_decrypt("vigenere")

            if (self.best_score < substitution_best_score):
                self.key = substitution_best_key
                self.best_score = substitution_best_score
                self.decrypted = substitution_best_decrypted
                self.intermediate_list = substitution_best_intermediate_list

    def bruteforce_decrypt(self, algorithm="substitution"):
        if algorithm == "caesar":
            # Generate the start key
            shift_val = self.keygen.get_initial_key("caesar")

            # Bruteforce all keys for Caesar cipher
            for _ in range(0, 26):
                if shift_val > 26:
                    shift_val = shift_val - 26

                # Try to decrypt the ciphertext
                decrypted_text = Encrypter.caesar_encrypt(
                    self.cypher_text, shift_val)

                # Compute and check the heuristic of the generated ciphertext
                score = self.fitness.score(decrypted_text)
                if score > self.best_score:
                    self.best_score = score
                    self.key = shift_val
                    self.decrypted = decrypted_text

                shift_val += 1

        elif algorithm == "substitution":
            # Generate the start key
            start_key = self.keygen.get_initial_key("substitution")

            iteration_count = 0
            for permutation in self.keygen.generate_key_permutation(start_key):
                # Try to decrypt the ciphertext
                decrypted_text = Encrypter.substitution_encrypt(
                    self.cypher_text, permutation)

                # Compute and check the heuristic of the generated ciphertext
                score = self.fitness.score(decrypted_text)
                if score > self.best_score:
                    self.best_score = score
                    self.key = permutation
                    self.decrypted = decrypted_text

                self.intermediate_list.append(score)

                if (iteration_count == MAX_ITERATIONS):
                    break
                iteration_count += 1

    def get_heuristic_values(self):
        list_len = len(self.intermediate_list)

        # Get only 100 or fewer scores to be sent to the user interface
        if (list_len <= 100):
            indexes = range(0, list_len)
            final_list = self.intermediate_list
        else:
            indexes = sorted(random.sample(range(0, list_len), 100))
            if (indexes[-1] != list_len - 1):
                indexes[-1] = list_len - 1
            final_list = [self.intermediate_list[index] for index in indexes]

        return (indexes, final_list)