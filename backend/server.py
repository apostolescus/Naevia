#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_cors import CORS
from encrypter import Encrypter
from decrypter import Decrypter

app = Flask(__name__)
CORS(app)


# Default route
@app.route("/")
def default_route():
    return "Naevia API\n"


# Encryption route
@app.route("/encrypt", methods=["GET"])
def encrypt_route():

    # Get arguments
    plaintext = request.args.get("plaintext", default="", type=str)
    cipher = request.args.get("cipher", default="", type=str)
    key = request.args.get("key", default="", type=str)

    # Encrypt
    ciphertext = ""
    if (cipher == "caesar"):
        ciphertext = Encrypter.caesar_encrypt(plaintext, int(key))
    elif (cipher == "vigenere"):
        ciphertext = Encrypter.vigenere_encrypt(plaintext, key)
    elif (cipher == "substitution"):
        ciphertext = Encrypter.substitution_encrypt(plaintext, key)

    # Return a result
    result = {"ciphertext": ciphertext}
    return jsonify(result)


# Decryption route
@app.route("/decrypt", methods=["GET"])
def decrypt_route():

    # Get arguments
    ciphertext = request.args.get("ciphertext", default="", type=str)
    strategy = request.args.get("strategy", default="", type=str)

    # Decrypt
    decrypter = Decrypter(ciphertext)
    if (strategy == "bruteforce"):
        decrypter.bruteforce_decrypt()
    elif (strategy == "hill-climbing"):
        decrypter.hillclimbing_decrypt()

    # Create heuristic dictionary
    heuristic_values = []
    (indexes, values) = decrypter.get_heuristic_values()
    for i in range(len(indexes)):
        heuristic_values.append({"x": indexes[i], "y": values[i]})

    # Return a result
    result = {
        "plaintext": decrypter.decrypted,
        "heuristic_values": heuristic_values
    }
    return jsonify(result)


def main():
    app.run(host="0.0.0.0", port=3001)


if __name__ == "__main__":
    main()