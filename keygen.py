from itertools import permutations 
import random

class KeyGen:

    def __init__(self):
        self.key_list = []

    def get_neighbours(self,string, size=2):
        neighbours = []

        for i in range(len(string)-size+1):
            subString = string[i:i+size]
            permutationsList = permutations(subString)
            for perm in list(permutationsList):
                result = string[:i]+''.join(perm)+string[i+size:]
                if string != result:
                    neighbours.append(result.upper())
        return neighbours

    def get_neighbours_vig(self, old_key, agressive = False):
        l = len(old_key)
        generated_keys = []
        
        if l>=4:
            if agressive is True:
                replace_letters = l/3
            else:
                replace_letters = l/4
        else:
            replace_letters = l/2

        for i in range(0,55):
            for k in range(0,int(replace_letters)):
                check = False

                while check is False:
                    position = random.randint(0,l-1)
                    new_val = random.randint(65,90)

                    while chr(new_val) == old_key[position]:
                        new_val = random.randint(65,90)
                    
                    new_key = old_key
                    new_key = new_key[:position]+ chr(new_val) + new_key[position+1:]
                
                    if new_key not in self.key_list:
                        self.key_list.append(new_key)
                        generated_keys.append(new_key)
                        check = True
       
        return generated_keys

    def get_neighbours_sub(self, old_key, neighbours_numbers, swap=1):

        l = len(old_key)
        key_list = []

        for j in range(0,int(neighbours_numbers)):
           
            check = False
            while check is False:
                new_key = ""
                for h in range(0, swap):
                    rand_val1 = 0
                    rand_val2 = 0
                    
                    while rand_val1 == rand_val2:
                        rand_val2 = random.randint(0, 99999)%l
                        rand_val1 = random.randint(0, 99999)%l
                    
                    if rand_val1 > rand_val2:
                        aux = rand_val1
                        rand_val1 = rand_val2
                        rand_val2 = aux

                    c1 = old_key[rand_val1]
                    c2 = old_key[rand_val2]

                    new_key = old_key[:rand_val1] + c2 + old_key[rand_val1 +1:rand_val2] + c1 + old_key[rand_val2+1:]
                
                if new_key not in self.key_list:
                    self.key_list.append(new_key)
                    check = True
                    key_list.append(new_key)

        return key_list

    def get_all(self,string):
        keys = []
        string = string.lower()
        for i in range(len(string)):
            letter = string[i]
            for j in range(26):
                word=string[:i]
                word+=chr(((ord(letter) % 97 +j )%26+ ord('a')))+string[i+1:]
                keys.append(word.upper())
        return keys

    def generate_key(self, algorithm, key_len=4):
       
        #CAESAR
        if algorithm == "caesar":
            n = random.randint(0,25)
            return n
        else:
            #VIGENERE
            if algorithm == "vig":
                keyV = ''
                for i in range(0,key_len):
                    n = random.randint(0,25)
                    keyV += chr(ord('A')+ n)
                # Daca vrei sa intorci un string
                return keyV
                
            #SUBSTITUTIE
            else:
                keyS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                keyS = list(keyS)
                random.shuffle(keyS)
                return "".join(keyS)

keygen = KeyGen()

# print(keygen.get_neighbours("ABCDEFGHEIJSADDASDASCAS"))
# print(keygen.get_all("abc"))
# keygen.get_neighbours_sub("ABCDEFGHEIJSADDASDASCAS")
