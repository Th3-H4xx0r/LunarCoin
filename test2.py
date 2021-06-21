# Imports
from Transaction import Transaction
from SignaturesECDSA import SignaturesECDSA
from SocketUtil import SocketUtil
import time 
import zlib
import requests
from progress.bar import Bar
# Global Variables
from BlockchainSyncUtil import BlockchainSyncUtil
from connections import Connections
import pickle
import hashlib

#myPrivate, myPublic = Signatures.generate_keys()
myPrivate, myPublic = SignaturesECDSA().loadKey()

addr, wif = SignaturesECDSA().make_address(myPublic.to_string())


sendPrivate = SignaturesECDSA().generateKeys()

sendPublic = sendPrivate.get_verifying_key()
addrSend, wifSend = SignaturesECDSA().make_address(sendPublic.to_string())

Tx = Transaction(myPublic, addr)
Tx.addOutput(addrSend, 0.00001)
Tx.sign(myPrivate)

hashData = pickle.dumps(Tx)

print(hashlib.sha256(hashData).hexdigest())

