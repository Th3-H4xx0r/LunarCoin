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
from SignaturesECDSA import SignaturesECDSA

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

            myPrivate, myPublic = SignaturesECDSA().loadKey()

            self.new_transaction('genesis', 'LC14NiTUSVd8FJbowK7G8g7yp3HwouNXkr8h', 10000, True)
            self.new_block(previous_hash=None)

            self.saveBlock()

        self.current_transactions = []


        self.verifyBlockchainIntegrity()

    
    def checkCoinsInCirculation(self):

        unser = self.chain

        balance = 0

        for block in unser:
            #print(block)

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


    def getBlockTXThreshold(self):

        TX_INTERVAL = 1000

        currentBlockCount = len(self.chain)

        txThreshold = 1

        for i in range(currentBlockCount):
            if(i % TX_INTERVAL == 0):
                if(i != 0):
                    txThreshold = txThreshold + 1

        #print(txThreshold)
        return txThreshold

    def goNewBlock(self):

        txThreshold = self.getBlockTXThreshold()

        if(len(self.current_transactions) >= txThreshold):
            #print("Going to next block with index: " + str(len(self.chain)))
            return True

        else:
            #print(str(len(self.current_transactions))  + "/" + str(txThreshold) + " transactions left until next block")
            return False



    def new_block(self, previous_hash=None):

        lastBlockHash = ''

        if(len(self.chain) == 0):
            lastBlockHash = ''
        
        else:
            lastBlockHash = self.computeHash(self.chain[-1])


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

    def verifyBlockchainIntegrity(self):

        valid = True

        lastHash = None

        print(len(self.chain))

        for i in range(len(self.chain)):


            if(i != 0):
                block_stringThis = pickle.dumps(self.chain[i])
                thisHash = hashlib.sha256(block_stringThis).hexdigest()

                print(str(self.chain[i].previousBlockHash) + " : " + str(lastHash))

                if(self.chain[i].previousBlockHash == lastHash):
                    print("Hash is correct")
                
                else:
                    valid = False
            
            block_string = pickle.dumps(self.chain[i])
            lastHash = hashlib.sha256(block_string).hexdigest()




            
        print(valid)


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
    def computeHash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = pickle.dumps(block)
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

        if(not isinstance(myPublic, str)):
            myPublic = myPublic.decode("utf-8") 

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

                        #print(tx['sender'] + " : " + myPublic + " --- " + str(type(tx['sender'])))

                        #print(tx['sender'])
                        #print(type(tx['recipient']))


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

    