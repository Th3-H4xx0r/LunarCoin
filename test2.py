import hashlib
import json
from os import dup
from threading import current_thread
from time import time
import pickle
from Block import Block
from Transaction import Transaction
from SocketUtil import SocketUtil
from Signatures import Signatures
import requests
from colorama import init 
from termcolor import colored 
import socket
from progress.bar import Bar
from SignaturesECDSA import SignaturesECDSA
from pymongo import MongoClient
import datetime
import ecdsa
from hashlib import sha256


client = MongoClient('localhost')
db=client.LunarCoin


def computeHash(block):
    """
    Creates a SHA-256 hash of a Block
    :param block: <dict> Block
    :return: <str>
    """

    # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
    block_string = pickle.dumps(block)
    return hashlib.sha256(block_string).hexdigest()

def getBlock(height):
    global db
    dataReturn = None

    data = db.Blockchain.find({'block_height': int(height)})

    for block in data:
        #print("BLOCK:" + str(block))
        dataReturn = block
    
    return dataReturn
    
def x():
    blocksHeight = self.get_current_block_length()

    bar = Bar('Verifying blockchain integrity', max=blocksHeight)
    
    valid = True

    try:

        lastHash = None

        for i in range(blocksHeight):

            currentBlock = getBlock(i)

            del currentBlock['_id']

            if(i > 0):

                if(currentBlock["previous_block"] == lastHash):
                    pass
                
                else:
                    print("Block " + str(i) + " is invalid")
                    valid = False
            
            lastHash = self.computeHash(currentBlock)
            bar.next()


        bar.finish()
        print("Blockchain is "+ str(valid))
    
    except Exception as e:
        print("Error with validating blockchain: " + str(e))
        valid = False

    return valid

print(x())