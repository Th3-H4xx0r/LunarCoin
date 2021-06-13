from SignaturesECDSA import SignaturesECDSA


#sk = SigningKey.generate(curve=SECP256k1)




'''

with open('keyAAAAA.dat', 'wb') as save:
    pickle.dump(sk, save)

with open('keyAAAAA.dat', 'rb') as save:
    sk = pickle.load(save)
'''
#print(sk)
sk = SignaturesECDSA().generateKeys()

SignaturesECDSA().saveKey(sk)
#SignaturesECDSA().saveKey()



vk = sk.get_verifying_key()

print(vk)


addr, wif = SignaturesECDSA().make_address(vk.to_string())

signature = sk.sign(b"message")

print(vk.verify(signature, b"message"))

print("Address: " + addr)
print("Privkey: " + wif)