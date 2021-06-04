# Imports
import hashlib
import json
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

init()

class Blockchain:

    x = 0
    current_transactions = []

    currentBlockCount = 0

    def __init__(self):

        try:
            with open('Blockchain/blockchain.dat', 'rb') as handle:
                self.chain = pickle.load(handle)
            
        except:

            print("Creating genesis block")

            self.chain = []
            
            # Create the genesis block

            myPrivate, myPublic = Signatures().load_key('privateKey.pem')

            self.new_transaction('genesis', b'-----BEGIN PUBLIC KEY-----\nMFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANN/zgMTrkYsV5Lc+ZrXJlWmt1GM+mue\nNupg/CPYQIBoXUi5ftB1kmz85u+7e9iH6lrurwtAGCu7bHTsjD4WGosCAwEAAQ==\n-----END PUBLIC KEY-----\n', 10000, True)
            self.new_block(previous_hash=None)

            self.saveBlock()

        self.current_transactions = []


    def getBlockTXThreshold(self):
        currentBlockCount = len(self.chain)

        txThreshold = 1

        for i in range(currentBlockCount):
            if(i % 5 == 0):
                txThreshold = txThreshold + 1

        return txThreshold

    def goNewBlock(self):

        txThreshold = self.getBlockTXThreshold()

        if(len(self.current_transactions) >= txThreshold):
            print("Going to next block with index: " + str(len(self.chain)))
            return True

        else:
            print(str(len(self.current_transactions))  + "/" + str(txThreshold) + " transactions left until next block")
            return False



    def new_block(self, previous_hash=None):

        lastBlockHash = ''

        if(len(self.chain) == 0):
            lastBlockHash = ''
        
        else:
            lastBlockHash = hash(self.chain[-1])


        block = Block(len(self.chain) + 1, time(), self.current_transactions, lastBlockHash)

        '''
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'previous_block': previous_hash or self.hash(self.chain[-1]),
        }
        '''

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)

        self.saveBlock()


        #return block


    def saveBlock(self):
        handle = open('Blockchain/blockchain.dat', 'wb')
        pickle.dump(self.chain, handle, protocol=pickle.HIGHEST_PROTOCOL)

        handle.close()

    def new_transaction(self, sender, recipient, amount, genesisBlock = False):

        if(genesisBlock):
            self.current_transactions.append({
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
            })

            
        else:

            self.current_transactions.append({
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
            })

            return self.last_block.index + 1

    def last_block_blockchain(self):
        return self.chain[-1]
         

    
    @property
    def last_block(self):
        return self.chain[-1]
    

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    def getBlockchain(url):
        r = requests.get(url)

        return eval(r.content)

    '''
    def getUserBalance(myPublic, apiServer = None, remoteBlockchain = False):

        data = None

        try:

            if(remoteBlockchain):

                print(apiServer)

                r = requests.get(apiServer + '/blockchain')

                #print(eval(r.content))

                data = eval(r.content)

            
            else:
                with open('blockchain.dat', 'rb') as handle:
                    data = pickle.load(handle)

                #if(r.ok):


            #print(data)

            #print(myPublic)

            try:

                unser = data

                chainLength = 0

                blockIndex = len(unser)

                balance = 0

                for block in unser:

                    transactions = None

                    try:
                        transactions = block['transactions']
                    except:
                        transactions = block.transactions


                    print(len(transactions))

            

                    for tx in transactions:

                        #print(tx)

                        # Checks if coins are being widthdrawed

                        print(tx['sender'] == myPublic)

                        print(tx['sender'])

                        if(tx['sender'] == myPublic):
                            #print("sender here")
                            #print(tx['amount'])

                            #print(tx)

                            try:
                                balance = balance - tx['amount']
                            
                            except:
                                balance = balance - tx.amount

                            #print(tx['amount'])
                            #print(tx.amount)
                            #print(balance)

                        
                        # Checks if coins are being deposited

                        if(tx['recipient'] == myPublic):
                            #print("Recipient here")
                            #print(tx['amount'])

                            #print(tx)
                            
                            try:
                                balance = balance + tx['amount']
                            
                            except:
                                balance = balance + tx.amount


                            #print(balance)

                    #chainLength = chainLength + 1

                    #currentBlock = unser[i - 1]

                    print("balance is: " + str(balance))
                    
                    return balance

            except Exception as e:
                print(colored("An error occured with getting a user's balance or a connection to the server could not be established: " + str(e), 'red'))
                return 0

            #else:
                #print(colored("[ERROR] Cannot connect to blockchain server", "red"))
                #return 0

        except Exception as e:
            print(colored("An error occured with getting a user's balance or a connection to the server could not be established: " + str(e), 'red'))
            return 0

'''

    def getUserBalance(self, myPublic, apiServer = None, remoteBlockchain = False):

        try:

            data = None

            if remoteBlockchain:
                r = requests.get(apiServer + '/blockchain')

                data = eval(r.content)

            else:
                
                data = self.chain

            #with open('blockchain.dat', 'rb') as handle:

            try:

                #print(data)

                unser = data

                balance = 0

                for block in unser:
                    #print(block)

                    transactions = None

                    if remoteBlockchain:

                        transactions = block['transactions']
                    
                    else:
                        transactions = block.transactions

                    for tx in transactions:

                        # Checks if coins are being widthdrawed

                        if(tx['sender'] == myPublic):

                            try:
                                balance = balance - tx['amount']
                            
                            except:
                                balance = balance - tx.amount


                        
                        # Checks if coins are being deposited

                        if(tx['recipient'] == myPublic):

                            
                            try:
                                balance = balance + tx['amount']
                            
                            except:
                                balance = balance + tx.amount


                #print("balance is: " + str(balance))
                    
                return balance

            except Exception as e:
                print(colored("An error occured with getting a user's balance or a connection to the server could not be established: " + str(e), 'red'))
                return 0

        except Exception as e1:
            print(colored("[FATAL ERROR] Error with fetching user balance: " + str(e1), "red"))

    