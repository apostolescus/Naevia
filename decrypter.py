from keygen import *
from collections import deque
import itertools
import ngram_score as ns
import sys

class decrypter:

    def __init__(self, cypher_text):
        self.cypher_text = cypher_text.upper()
        self.keygen = KeyGen()
        self.fitness = ns.heuristic('quadgrams')
        self.best_score = -sys.maxsize - 1
        self.key = ""
        self.decrypted = ""
        self.intermediate_list = []
        self.preprocess_text()

    #decrypt vigenere and substitution
    def hillclimbing_decrypt(self, algorithm, key_len=4, boost = False):

        check = False
        key = ""
        if algorithm == "vig":
            key = self.keygen.generate_key("vig", key_len)
        elif algorithm == "sub":
            key = self.keygen.generate_key("sub")
        else:
            return
        
        while check is False:
            check = True
            if algorithm == "vig":
                generated_keys = self.keygen.get_neighbours_vig(key, boost)
            else:
                generated_keys = self.keygen.get_neighbours_sub(key, 300, 3)
            
            for k in generated_keys:
                if algorithm == "vig":
                    decrypted_text = self.decrypt_vigenere(k)
                else:
                    decrypted_text = self.decrypt_substitution(k)

                entropy = self.fitness.score(decrypted_text)

                if entropy > self.best_score:
                    self.best_score = entropy
                    self.key = k
                    self.decrypted = decrypted_text
                    self.intermediate_list.append((entropy, key))
                    
                    if len(self.intermediate_list) >= 100:
                        self.process_list()
                    key = k
                    check = False
      
        # print("decrypted is: ", self.decrypted)
        # print("key is: ", self.key)
        return self.intermediate_list

    def bruteforce_decrypt(self,name, key_len=4):

        if name == "caesar":
            shift_val = self.keygen.generate_key("caesar")
            for i in range(0,26):
                if shift_val > 26:
                    shift_val = shift_val - 26

                decrypted_text = self.decrypt_caesar(shift_val)
                score = self.fitness.score(decrypted_text)

                if score > self.best_score:
                    self.best_score = score
                    key = shift_val

                shift_val+=1

            self.key = key
            self.decrypted = self.decrypt_caesar(key)
            return 
        
        elif name == "sub":
            start_key = self.keygen.generate_key("sub")
            self.generate_permutation(start_key)

        # elif name == "vig":
        #     tested_list = []
        #     elem = "ABCD"
        #     print("alg is:", name)

    def generate_permutation(self, text):
        # convert string to list of char to allow swapping
        print("You just started a brute force on a 26 char long string.\n"+
        "Wish u good luck! It is said that none lived to see the end!")
        self._generate_permutation(list(text), 0, len(text)-1)

    def _generate_permutation(self, text, start, end):
        # base
        if start == end:
            
            permutations = ''.join(text)
            decrypter_text = self.decrypt_substitution(permutations)
            score = self.fitness.score(decrypter_text)

            if score > self.best_score:
                self.best_score = score
                self.key = permutations
                print("score is: ", score, "key is: ", self.key)
        
            return

        for i in range(start, end+1):
            text[start], text[i] = text[i], text[start]
            self._generate_permutation(text, start+1, end)
            # backtrack like a tree, to restore previous state
            text[start], text[i] = text[i], text[start]

    def decrypt_caesar(self, key):
        
        decrypted_text = ""
        for char in self.cypher_text:
            char = ord(char.upper()) % 65
            decrypt = (char + key) % 26
            decrypted_text += chr(decrypt + 65)
        return decrypted_text

    def decrypt_vigenere(self, key):
        l = len(self.cypher_text)
        final_key = ""
        decrypted_text = ""

        if len(key) < l:
            final_len = len(key)
            c = int(l/final_len)
            r = l%final_len

            for i in range(0,c):
                final_key += key
            if r != 0:
                final_key += key[:r]
        
        for i in range(0,l):
                d = ord(self.cypher_text[i])%26 - ord(final_key[i])%26
                if d<0:
                    d += 26
                decrypted_text += chr(d + ord("A"))

        return decrypted_text

    def preprocess_text(self):
        processed_text = ""
        for j in self.cypher_text:
            if j.isalpha():
                processed_text += j
        self.cypher_text = processed_text

    def process_list(self):
        new_list = []

        for i in range(0,100,10):
            new_list.append(self.intermediate_list[int(i)])
        
        self.intermediate_list = new_list

    def decrypt_substitution(self, key):
        l = len(self.cypher_text)
        decrypted_text = ""

        for i in self.cypher_text:
            index = key.find(i)
            decrypted_c = chr(index + ord("A"))
            decrypted_text += decrypted_c

        return decrypted_text

#substitution

# dc = decrypter("QPGCFXCPEGFFKXGTVGFFQOGUVKEUGZTGRGCVGFDTKPIKPIAQWQ"+
# "NFRQUUKDNGRTQEWTGFJGTVTKHNKPINCWIJVGTVJQWIJVURTQRGTVAUJGOGVYCAEQO"+
# "RCPKQPUUJAJCFUQNKEKVWFGHCXQWTCDNGQYPYJKEJEQWNFUCYIWGUVOCPPQYJGCTFDWVNC"+
# "UVGFOAEQOKPIWPGCUAOCTMGFUQUJQWNFITCXKVANGVVGTUKVCOQPIUVJGTUGNHFGCTGUVCPYKPF"+
# "QYUDAYQQFGFNCFKGUUJGDCUMGVUGCUQPCIGJGTWP"
# +"GCUAUCYFKUEQWTUGWPYKNNKPICOPQFGUETKDGFFGLGEVKQPKPEQOOQFGPQNKUVGPKPIQHDGHQTGCVWTGJKURCTKUJDQA")
# dc.hillclimbing_decrypt("sub")
# print(dc.key)

#substitution brute force

# dc.bruteforce_decrypt("sub")
# print(dc.decrypted)


#caesar

# dc = decrypter("Pmolohkhufaopunjvumpkluaphsavzhfoldyvalpapujpwolyaohapzifzvjohunpunaolvyklyvmaolslaalyzvmaolhswohilaaohauvahdvykjvbskilthklvba")
# dc.bruteforce_decrypt("caesar")
# print("text is: ", dc.decrypted)

#vig nu mai stiu cum; key: ANNAMM

# dc = decrypter("Fbylk ioeqs iudbj ozq dbjne rej ngq qvrey eqvra. Ir yiff pmdt ol fmot ur pmdk whsf ehrj. Duecbiedqd und sqt pbneudreep brbweofiba wta fniogdaoye. Zqcrfsmdy hc kzawyrdsq ig goxqrnolk. Gnjvlxunt qebmrghrq qdhpafuoa vs nq dnfhiaoqf od mn. Hfe arf ntrqqaoye xmw hawuxlvag eur qrfuoirat ogrvbsufy vasfmngyy. Qmsl zizp lvse rmcg jift srr hme bbee fqn. Cnrueh nay otaggy omn ryizar qvrqot sbr rarzrr. Gb af zemzt jvdai edhax mn fuadq lrnsf. ")
# dc.hillclimbing_decrypt("vig", key_len = 6)
# print(dc.key)

