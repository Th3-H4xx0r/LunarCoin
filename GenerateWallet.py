# Imports
from Signatures import Signatures
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

from cryptography.hazmat.primitives import serialization
import os.path
from os import path


try:
    exists = path.exists("privateKey.pem")

    if(exists):
        print("Wallet already exists. Cannot create new one unless old one is deleted. Delete privateKey.pem if you want to create a new wallet.")
    else:
        myPrivate, myPublic = Signatures.generate_keys()

        Signatures().save_key(myPrivate)

        print("New wallet created")

except Exception as e:
    print("An error has occured: " + str(e))
