# imports
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

from cryptography.hazmat.primitives import serialization


class Signatures:
    def generate_keys():
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

        return private, pu_ser


    def sign(message, private):
        signature = private.sign(
            bytes(str(message), 'utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        #print(signature)
        return signature


    def verify(message, sig, pu_ser):

        public = serialization.load_pem_public_key(
            pu_ser,
            backend=default_backend()
        )

        message = bytes(str(message), 'utf-8')

        try:
            public.verify(
                sig,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            return True


        
        except InvalidSignature as e:
            return False

        except Exception as e:
            print("Error with verify function: " + str(e))
            return False
    
    def save_key(self, pk):
        pem = pk.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        
        with open('privateKey.pem', 'wb') as pem_out:
            pem_out.write(pem)

        '''
        public_key = pk.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
        )

        with open('publicKey.pem', 'wb') as pem_out:
            pem_out.write(public_key)
        '''
    

    def load_key(self, pr):

        public_key = None
        private_key = None

        with open(pr, "rb") as kf:
            private_key = serialization.load_pem_private_key(
                kf.read(),
                password=None,
                backend=default_backend()
            )

            #print(private_key)

            public = private_key.public_key()


            public_key = public.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            
            #print(public_key)

        return private_key, public_key
        


if __name__ == "__main__":
    pr, pu = generate_keys()

    message = b"Hello World!"
    signature = sign(message, pr)

    correct = verify(message, signature, pu)



    if correct:
        print("Signature is valid")

    else:
        print("Signature is WRONG")


