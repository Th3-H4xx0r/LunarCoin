# Imports
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


init()

class BlockchainMongo:

    x = 0
    current_transactions_mempool = []

    currentBlockCount = 0

    client = MongoClient('localhost')
    db=client.LunarCoin

    def __init__(self):

        try: 

            if('Blockchain' in self.db.list_collection_names()): # Checks if blockchain exists
                # Exists

                if(self.db.Blockchain.estimated_document_count() == 0): # Checks if collection is not empty
                    print("Creating blockchain genesis block. Current chain is currupted or does not exist")

                    # Creates genesis block

                    self.new_transaction('genesis', 'LC14NiTUSVd8FJbowK7G8g7yp3HwouNXkr8h', 10000, '0x000000000000000000000000000000000000000000000000', time(), '0x0', True)
                    self.new_block(previous_hash=None)
                
                else:
                    pass

            else:
                self.db["Blockchain"] # Creates blockchain


                print("Blockchain is corrupted or file does not exist.")

                print("Creating genesis block")
                
                # Create the genesis block

                myPrivate, myPublic = SignaturesECDSA().loadKey()

                #sender, recipient, amount, transactionID, timestamp, hashVal

                self.new_transaction('genesis', 'LC14NiTUSVd8FJbowK7G8g7yp3HwouNXkr8h', 10000, '0x000000000000000000000000000000000000000000000000', time(), '0x0', True)
                self.new_block(None, previous_hash=None)

                #self.saveBlock(block)

            
            self.current_transactions_mempool = []
                

           #chain = self.db.Transactions.estimated_document_count()

            
        except Exception as e:
            print("Fatal error with blockchain init: " + str(e))


        #valid = self.verifyBlockchainIntegrity()

        #if(valid == False):
            #raise("Blockchain invalid")

    
    def checkCoinsInCirculation(self):

        unser = self.chain

        balance = 0

        for block in unser:

            transactions = block.transactions

            for tx in transactions:

                # Checks if coins are being widthdrawed

                #print(tx['sender'] + " : " + myPublic + " --- " + str(type(tx['sender'])))

                #print(tx['sender'])
                #print(type(tx['recipient']))

                if(tx['sender'] == 'genesis'):
                    balance = balance + tx['amount']


                if(tx['sender'] == 'validator_reward'):
                    balance = balance + tx['amount']




        print("Coins in circulation: " + str(balance))
            
        return balance

    def blockConsensusProtocol(self, block, peers):

        # If more than 50% of the nodes accept the block, it is added to the chain

        for peer in peers:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((peer['ip'], peer['port']))


            data = pickle.dumps(b'block_confirmation:' + pickle.dumps(block))


            s.sendall(data)

            # Peers send back their block and a confirmation

            blockTemp = b''

            while True:
                packet = s.recv(6553611)
                blockTemp += packet
                if not packet: break
            
            blockData = pickle.loads(blockTemp)

            print(blockData)

            









    def getBlockTXThreshold(self):



        TX_INTERVAL = 1000

        currentBlockCount = self.get_current_block_length()

        txThreshold = 1

        for i in range(currentBlockCount):
            if(i % TX_INTERVAL == 0):
                if(i != 0):
                    txThreshold = txThreshold + 1

        #print(txThreshold)
        #print("Block threshold: " + str(txThreshold))
        return txThreshold

    def goNewBlock(self):

        txThreshold = self.getBlockTXThreshold()

        if(len(self.current_transactions_mempool) >= txThreshold):
            #print("Going to next block")

            return True

        else:
            print(str(len(self.current_transactions_mempool))  + "/" + str(txThreshold) + " transactions left until next block")
            return False

    def getBlock(self, height):
        dataReturn = None

        data = self.db.Blockchain.find({'block_height': int(height)})

        for block in data:
            #print("BLOCK:" + str(block))
            dataReturn = block
        
        return dataReturn

    def get_current_block_length(self):
        return self.db.Blockchain.estimated_document_count()
    
    def get_previous_block(self, currentHeight):
        docs = self.db.Transactions.find({"block_height": currentHeight - 1 })

        block = None

        for doc in docs:
            block = doc

        return block


    def new_block(self, VALIDATOR_PEERS, previous_hash=None):

        try:

            lastBlockHash = ''

            currentHeight = self.get_current_block_length()

            if(currentHeight == 0): # Genesis block
                lastBlockHash = ''
            
            else:
                lastBlockHash = self.computeHash(self.get_previous_block(currentHeight))
            

            #block = Block(len(self.chain) + 1, time(), self.current_transactions, lastBlockHash)

            # TODO: FOR block confirmation
            '''
                        block_tmp = {
                'block_height': currentHeight,
                'transactions': self.current_transactions_mempool,
                'previous_block': lastBlockHash,
            }

            if(VALIDATOR_PEERS != None):
                self.blockConsensusProtocol(block_tmp, VALIDATOR_PEERS)
            

            '''

            block = {
                'block_height': currentHeight,
                'timestamp': time(),
                'transactions': self.current_transactions_mempool,
                'previous_block': lastBlockHash,
            }
            

            # Reset the current mempool of transactions
            self.current_transactions_mempool = []


            #self.chain.append(block)



            self.saveBlock(block)


            #return block
        except Exception as e:
            print("Error with adding block to the chain: " + str(e))

    def verifyBlockchainIntegrity(self): 


        bar = Bar('Verifying blockchain integrity', max=len(self.chain))

        
        valid = True

        try:


            lastHash = None

            print(len(self.chain))

            for i in range(len(self.chain)):


                if(i != 0):
                    block_stringThis = pickle.dumps(self.chain[i])
                    thisHash = hashlib.sha256(block_stringThis).hexdigest()

                    #print(str(self.chain[i].previousBlockHash) + " : " + str(lastHash))

                    if(self.chain[i].previousBlockHash == lastHash):
                        #print("Hash is correct")
                        pass
                    
                    else:
                        valid = False
                
                block_string = pickle.dumps(self.chain[i])
                lastHash = hashlib.sha256(block_string).hexdigest()
                bar.next()


            bar.finish()
            print("Blockchain is "+ str(valid))
        
        except Exception as e:
            print("Error with validating blockchain: " + str(e))
            valid = False

        return valid


    def saveBlock(self, block):
        self.db.Blockchain.insert(block)
    
    def saveBlockStatic(block):
        try:
            client = MongoClient('localhost')
            db=client.LunarCoin
            db.Blockchain.insert(block)
        
        except Exception as e:
            print("Error adding block to the chain: " + str(block['block_height']))
            pass
    
    def deleteBlockchainStatic():
        client = MongoClient('localhost')
        db=client.LunarCoin
        db.Blockchain.delete_many({})
        print("Deleted current blockchain")


    def new_transaction(self, sender, recipient, amount, transactionID, timestamp, hashVal, genesisBlock = False):

        #print("Lenght of transactions: " + str(len(self.current_transactions)))

        if(genesisBlock):
            self.current_transactions_mempool.append({
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
                'transactionID': transactionID,
                'timestamp': timestamp,
                'hash': '0x0' #TODO: Add hash
            })

            
        else:

            self.current_transactions_mempool.append({
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
                'transactionID': transactionID,
                'timestamp': timestamp,
                'hash': hashVal
            })

            #return self.last_block.index + 1

    def last_block_blockchain(self):
        return self.chain[-1]
         

    
    @property
    def last_block(self):
        return self.chain[-1]
    

    @staticmethod
    def computeHash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = pickle.dumps(block)
        return hashlib.sha256(block_string).hexdigest()


    def getUserBalance(self, myPublic, checkTransactionID=None):

        duplicate = False

        try:

            if(type(myPublic) != str):
                myPublic = myPublic.decode('utf-8')


            #print(myPublic)


            outgoingTx = self.db.Blockchain.find({"transactions.sender": myPublic })

            incomingTx = self.db.Blockchain.find({"transactions.recipient": myPublic })

            balance = 0

            # Checks outgoing transactions

            for outTxBlock in outgoingTx:
                transactions = outTxBlock['transactions']

                for tx in transactions:
                    if(tx['sender'] == myPublic):

                        if(tx['transactionID'] == checkTransactionID):
                            duplicate = True

                        try:
                            balance = balance - tx['amount']
                        
                        except:
                            balance = balance - tx.amount
            

            # Checks incoming transactions

            for incomingTxBlock in incomingTx:
                transactions = incomingTxBlock['transactions']

                for tx in transactions:
                    if(tx['recipient'] == myPublic):

                        if(tx['transactionID'] == checkTransactionID):
                            duplicate = True

                        try:
                            balance = balance + tx['amount']
                        
                        except:
                            balance = balance + tx.amount
            

            #print("BALANCE: " + str(balance))
            return balance, duplicate

        except Exception as e:
            print(colored("[FATAL ERROR] Error with fetching user balance: " + str(e), "red"))

        
