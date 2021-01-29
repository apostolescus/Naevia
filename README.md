# Naevia

## Description

**Naevia** is a platform demonstrating the usage of the **Hill Climbing** optimization technique (only for local optima solutions) and **N-grams frequency** for **cryptanalysis**. Its functionalities, which are available through a web interface, are:
- encryption with classic ciphers:
  - Caesar;
  - Vigenere;
  - substitution;
- decryption via:
  - brute-force;
  - Hill Climbing.

### Observations

To improve the convergence to the solution (the real plaintext), the following **preliminary steps** can be done:
- running the decryption multiple time (it starts at each run from a different random value, maybe God will have mercy on you once);
- increase ciphertext size (*if possible*); and
- shorten key length (*if possible*).

Limitations of the current version of the platform are some fixed parameters:
- the N-grams length (`4`);
- the number of keys generated into the brute-force process (`3500`); and
- the length of the Vigenere key that is brute-forced (`12`).

### Demos

1. [Encryption with the substitution cipher. Decryption via brute-foce](others/demos/bruteforce/substitution.mp4)
2. [Encryption with the Caesar cipher. Decryption via Hill Climbing](others/demos/hill_climbing/caesar.mp4)
3. [Encryption with the Vigenere cipher. Decryption via Hill Climbing](others/demos/hill_climbing/caesar.mp4)
4. [Encryption with the substitution cipher. Decryption via Hill Climbing](others/demos/hill_climbing/caesar.mp4)

## Setup

1. install [Python3](https://www.python.org/downloads/) and [Node.js](https://nodejs.org/en/download/)
2. set up and run the server

```
cd backend
pip3 install -r requirements.txt
python3 server.py
```

3. set up and run the user interface

```
cd user-interface
npm install
npm start
```

## Resources

### User Interface

- [React](https://reactjs.org/)
- [React Bootstrap](https://react-bootstrap.github.io/)
- [axios](https://github.com/axios/axios)
- [Victory](https://formidable.com/open-source/victory/)
- [React Icons](https://react-icons.github.io/react-icons)
- logo from [Icons8](https://icons8.com/)
- background animation from [CodePen](https://codepen.io/mohaiman/pen/MQqMyo)

### Backend

- [Python3](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/)

## Further Improvements

- [ ] solving the above mentioned limitations
- [ ] more parameter tuning