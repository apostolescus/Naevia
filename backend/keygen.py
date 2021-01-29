from itertools import permutations
import random


class KeyGen:
    def __init__(self):
        self.key_list = []

    @staticmethod
    def get_neighbours(string, size=2):
        neighbours = []

        for i in range(len(string) - size + 1):
            subString = string[i:i + size]
            permutationsList = permutations(subString)
            for perm in list(permutationsList):
                result = string[:i] + "".join(perm) + string[i + size:]
                if string != result:
                    neighbours.append(result.upper())

        return neighbours

    def get_neighbours_vigenere(self, old_key, agressive=False):
        l = len(old_key)
        generated_keys = []

        if l >= 4:
            if agressive is True:
                replace_letters = l / 3
            else:
                replace_letters = l / 4
        else:
            replace_letters = l / 2

        for _ in range(0, 55):
            for _ in range(0, int(replace_letters)):
                check = False

                while check is False:
                    position = random.randint(0, l - 1)
                    new_val = random.randint(65, 90)

                    while chr(new_val) == old_key[position]:
                        new_val = random.randint(65, 90)

                    new_key = old_key
                    new_key = new_key[:position] + chr(
                        new_val) + new_key[position + 1:]

                    if new_key not in self.key_list:
                        self.key_list.append(new_key)
                        generated_keys.append(new_key)
                        check = True

        return generated_keys

    def get_neighbours_substitution(self, old_key, neighbours_numbers, swap=1):
        l = len(old_key)
        key_list = []

        for _ in range(0, int(neighbours_numbers)):
            check = False

            while check is False:
                new_key = ""
                for _ in range(0, swap):
                    rand_val1 = 0
                    rand_val2 = 0

                    while rand_val1 == rand_val2:
                        rand_val2 = random.randint(0, 99999) % l
                        rand_val1 = random.randint(0, 99999) % l

                    if rand_val1 > rand_val2:
                        aux = rand_val1
                        rand_val1 = rand_val2
                        rand_val2 = aux

                    c1 = old_key[rand_val1]
                    c2 = old_key[rand_val2]

                    new_key = old_key[:rand_val1] + c2 + old_key[
                        rand_val1 + 1:rand_val2] + c1 + old_key[rand_val2 + 1:]

                if new_key not in self.key_list:
                    self.key_list.append(new_key)
                    check = True
                    key_list.append(new_key)

        return key_list

    @staticmethod
    def get_all(string):
        keys = []
        string = string.lower()

        for i in range(len(string)):
            letter = string[i]

            for j in range(26):
                word = string[:i]
                word += chr(
                    ((ord(letter) % 97 + j) % 26 + ord("a"))) + string[i + 1:]
                keys.append(word.upper())

        return keys

    @staticmethod
    def get_initial_key(algorithm, key_len=4):
        if algorithm == "caesar":
            key = random.randint(0, 25)
        elif algorithm == "vigenere":
            key = ""
            for _ in range(0, key_len):
                key += chr(ord("A") + random.randint(0, 25))
        else:
            key = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            random.shuffle(key)
            key = "".join(key)

        return key

    @staticmethod
    def generate_key_permutation(key):
        """Narayana Pandita"s algorithm for generation of all permutation in
        lexicographic order
        
        Source: https://izziswift.com/finding-all-possible-permutations-of-a-given-string-in-python/
        """
        a = sorted(key)
        n = len(a) - 1
        while True:
            yield "".join(a)

            for j in range(n - 1, -1, -1):
                if a[j] < a[j + 1]:
                    break
            else:
                return

            k = 0
            v = a[j]
            for k in range(n, j, -1):
                if v < a[k]:
                    break

            a[j], a[k] = a[k], a[j]
            a[j + 1:] = a[j + 1:][::-1]