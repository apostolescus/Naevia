# Naevia


### decrypter.py

Decypter class can perform the following opperations:
1. *decrypt Vigenere ciphertext with given key length using hill-climbing algorithm*
2. *decrypt Caesar ciphertext using brute force*
3. *decrypt Substitution ciphertext using brute force (not recommended)*
4. *decrypt Substitution ciphertext using hill-climbing algorithm*

Decrypt uses quadgrams for heuristic calculation.
#### How to use

First of all create an object of decrypter class.
When initializating the object you should provide the text you want to decrypt.

        from decrypter.py import decrypter
        
        dc = decrypter("Fbylk ioeqs iudbj ozq")
        
In order to decrypt the text you should call one of the following methods:
brute_force_decrypt() or hillclimbing_decrypt().
    
**brute_force_decrypt(algorithm_name)** where:
* algorithm_name : caesar or sub (for substitution)

**hillclimbing_decrypt(algorithm, key_len, boost):intermediate_list** where:
* algorithm : vig or sub
* key_len: vigenere key length; it is set by default to 4
* boost: boolean value; set by default to False
    Boost allows to increase the randomness of the new generated keys. This means that you can descend faster, with bigger steps, but with lower precision. 
* returns all the keys and their heuristics

The  decrypted object stores the following:
1. decrypted text (*object.decrypted*)
2. lowest heuristic (*object.best_score*)
3. list with all keys and heuristics (*object.intermediate_list*)
4. final key (*object.key*)

### Example
    
        dc = decrypter("cypher_text")
        dc.bruteforce_decrypt("caesar")
        print("text is: ", dc.decrypted)
        
OR
        
        dc = decrypter("cipher_text ")
        dc.hillclimbing_decrypt("vig", key_len = 6)
        print("key is:", dc.key)
        
### Didn't find the key?

Given the fact that the algorithm finds the local minimum, it may not find the correct key on the first try.
It is recomended to run it multiple times because it always starts with a random value, thus increasing the chances of finding the right key.
In order to improve key detection try the following:
* increase cipher text size
* shorten key length (if possible)
* run it multiple times (maybe God will have mercy on you once)



### Futher implementations
* brute force for vigenere
* monograms heuristic
* allow for more parameter tuning
