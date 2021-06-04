# Imports
import hashlib
import json
from time import time
import pickle

class Block:

    def __init__(self, index, timestamp, transactions, previousBlockHash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previousBlockHash = previousBlockHash

    def __repr__(self):
        return str({'index': self.index, 'timestamp': self.timestamp, 'transactions': self.transactions, 'previousBlockHash': self.previousBlockHash})

