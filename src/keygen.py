from itertools import permutations 

class  KeyGen:

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

keygen = KeyGen()

#print(keygen.get_neighbours("ABCD"))
print(keygen.get_all("abc"))
