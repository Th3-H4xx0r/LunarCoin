from cryptography.hazmat.primitives import serialization
# imports
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

from cryptography.hazmat.primitives import serialization
import json
import hashlib

x = 324234

block_string = json.dumps(x, sort_keys=True).encode()
x1 = hashlib.sha256(block_string).hexdigest()

print(x1)