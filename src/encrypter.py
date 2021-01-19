class Ecrypter:
    
    def remove_Spaces(self, plaintext):
        noSpaces=""
        for i in range(len(plaintext)):
            if plaintext[i] != ' ':
                noSpaces+=plaintext[i]
        return noSpaces

    def caesar(self, plaintext, key):
        cipher=""
        plaintext = plaintext.upper()
        for i in range(len(plaintext)):
            letter = plaintext[i]
            cipher +=chr((ord(letter)+key - 65)%26+65)
        return cipher
    
    def vigenere(self, plaintext, key):
        if(len(plaintext) != len(key)):
            print ("Lengths must be equal")
            return -1
        plaintext = plaintext.upper()
        key = key.upper()   
        cipher=""
        for i in range(len(plaintext)):
            cipher+=chr((ord(plaintext[i])+ord(key[i]))%26 + ord('A'))
        return cipher

    def substitute(self,plaintext, key):
        
        plaintext = self.remove_Spaces(plaintext)
        plaintext = plaintext.upper()
        key = key.upper() 
        keyLen = len(key)  
        cipher=""
        for i in range(len(plaintext)):
            cipher+=chr((ord(plaintext[i])+ord(key[i%keyLen]))%26 + ord('A'))
        return cipher


enc = Ecrypter()
cipherCaesar = enc.caesar(t,4)
cipherVigenere = enc.vigenere("code","team")
cipherSubstitute = enc.substitute("ana are mere","abc")
print(cipherSubstitute)