from cryptography.hazmat.primitives import serialization
# imports
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

from cryptography.hazmat.primitives import serialization


private = rsa.generate_private_key(
    public_exponent=65537,
    key_size=512,
    backend=default_backend()
)

public = private.public_key()

pu_ser = public.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)



print(pu_ser)