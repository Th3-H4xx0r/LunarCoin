import time
import random
import secrets
import hashlib
from hashlib import sha256

import os
import pickle
from ecdsa import SigningKey, SECP256k1
from ecdsa import VerifyingKey
import binascii

class SignaturesECDSA:

    def __init__(self):
        self.P = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1
        self.G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
        0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
        self.B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    def ripemd160(self, x):
        d = hashlib.new("ripemd160")
        d.update(x)
        return d

    def point_add(self, p, q):
        xp, yp = p
        xq, yq = q

        if p == q:
            l = pow(2 * yp % self.P, self.P - 2, self.P) * (3 * xp * xp) % self.P
        else:
            l = pow(xq - xp, self.P - 2, self.P) * (yq - yp) % self.P

        xr = (l ** 2 - xp - xq) % self.P
        yr = (l * xp - l * xr - yp) % self.P

        return xr, yr


    def point_mul(self, p, d):
        n = p
        q = None

        for i in range(256):
            if d & (1 << i):
                if q is None:
                    q = n
                else:
                    q = self.point_add(q, n)

            n = self.point_add(n, n)

        return q


    def point_bytes(self, p):
        x, y = p

        return b"\x04" + x.to_bytes(32, "big") + y.to_bytes(32, "big")


    def b58_encode(self, d):
        out = ""
        p = 0
        x = 0

        while d[0] == 0:
            out += "1"
            d = d[1:]

        for i, v in enumerate(d[::-1]):
            x += v * (256 ** i)

        while x > 58 ** (p + 1):
            p += 1

        while p >= 0:
            a, x = divmod(x, 58 ** p)
            out += self.B58[a]
            p -= 1

        return out
    
    def generateKeys(self):
        signing_key = SigningKey.generate(curve=SECP256k1)
        return signing_key
    
    def saveKey(self, sk):
        sk_pem = sk.to_pem()

        with open("key.pem", "wb") as f:
            f.write(sk_pem)

    def loadKey(self):
        try:
            with open("key.pem") as f:
                vk1 = SigningKey.from_pem(f.read())

                verifyingKey = vk1.get_verifying_key()
                return vk1, verifyingKey
        
        except: 
            print("Error with loading private key")
            return None, None
    
    def signRaw(self, data, pk):
        try:
            signature = pk.sign(data)
            return signature
        
        except Exception as e:
            print("Error with verifying signature: " + str(e))
            return False
        
    def sign(self, data, pk):
        
        try:
            signature = pk.sign(bytes(str(data), 'utf-8'))
            return signature
        
        except Exception as e:
            print("Error with verifying signature: " + str(e))
            return False
    
    def verify(self, message, sig, verifyingKey):
        return verifyingKey.verify(sig, message)

    def make_address(self, privkey):
        q = self.point_mul(self.G, int.from_bytes(privkey, "big"))
        hash160 = self.ripemd160(sha256(self.point_bytes(q)).digest()).digest()
        addr = b"\x00" + hash160
        checksum = sha256(sha256(addr).digest()).digest()[:4]
        addr += checksum

        wif = b"\x80" + privkey
        checksum = sha256(sha256(wif).digest()).digest()[:4]
        wif += checksum

        addr = self.b58_encode(addr)
        wif = self.b58_encode(wif)
        
        addr = "LC" + addr  # Adds the 'LC' to the start of the address
        return addr, wif
    
    def generateRandomID_98_digit(self):
        return (b'0x' + binascii.b2a_hex(os.urandom(48))).decode()
    
    def generateHex82igit(self):
        return (b'0x' + binascii.b2a_hex(os.urandom(40))).decode()