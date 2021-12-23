# Imports
import hashlib
import json
from os import dup
from threading import current_thread
from time import time
import time as timeFunc
import pickle
import traceback
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
import sys

init()

class BlockchainMongo:

    x = 0
    current_transactions_mempool = []

    currentBlockCount = 0

    client = MongoClient('localhost')
    db=client.LunarCoin

    util = SocketUtil()


    def __init__(self):
        pass

    
    def initializeBlockchain(self):
        try: 

            if('Blockchain' in self.db.list_collection_names()): # Checks if blockchain exists
                # Exists

                if(self.db.Blockchain.estimated_document_count() == 0): # Checks if collection is not empty
                    print("Creating blockchain genesis block. Current chain is currupted or does not exist")

                    # Creates genesis block

                    self.new_transaction('genesis', 'LC14NiTUSVd8FJbowK7G8g7yp3HwouNXkr8h', 10000, '0x000000000000000000000000000000000000000000000000', time(), '0x0', 'none', 'none', 'metadata', True)
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

                self.new_transaction('genesis', 'LC14NiTUSVd8FJbowK7G8g7yp3HwouNXkr8h', 10000, '0x000000000000000000000000000000000000000000000000', time(), '0x0', 'none', 'none', 'metadata', True)
                self.new_block(None, previous_hash=None)

                #self.saveBlock(block)

            
            self.current_transactions_mempool = []
                

            #chain = self.db.Transactions.estimated_document_count()


            ###########################
            ## InvoicePool Initilization
            ###########################

            if('InvoicePool' not in self.db.list_collection_names()): # Checks if InvoicePool exists
                self.db["InvoicePool"] # Creates InvoicePool
            
        except Exception as e:
            print("Fatal error with blockchain init: " + str(e))


        #valid = self.verifyBlockchainIntegrity()

        #if(valid == False):
            #print(colored("[BLOCKCHAIN] Blockchain is invalid", "red"))


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

            #print(blockData)

    def getBlockTXThreshold(self):
        '''
        @ Implementation
         - The transaction threshold increases by 1 for 100 blocks (with block 1 having a tx threshold of 1)
         The following equation can be used to find the block tx threshold (rounding down to the last whole number)
            - f(x) = (x/100-1) + 1 
            - f(x) = transaction threshold for block (x)
        '''
        TX_INTERVAL = 100
        currentBlockCount = self.get_current_block_length()
        txThreshold = 1
        for i in range(currentBlockCount):
            if(i % TX_INTERVAL == 0):
                if(i != 0):
                    txThreshold = txThreshold + 1
        return txThreshold

    def goNewBlock(self):
        txThreshold = self.getBlockTXThreshold()
        if(len(self.current_transactions_mempool) >= txThreshold):
            return True
        else:
            print(str(len(self.current_transactions_mempool))  + "/" + str(txThreshold) + " transactions left until next block")
            return False

    def getBlock(self, height):
        dataReturn = None
        data = self.db.Blockchain.find({'block_height': int(height)})
        for block in data:
            dataReturn = block
        return dataReturn
    
    def getBlockStatic(db, height):
        dataReturn = None
        data = db.Blockchain.find({'block_height': int(height)})
        for block in data:
            dataReturn = block
        return dataReturn
    
    def verifyTransactionBlockchainIntegrity(self, tx, currentBlock):
        try:
            execute = False
            if(tx['sender'] != 'genesis' and tx['sender'] != 'validator_reward'):
                valid = False

                print("TRYING 1")
                publicKey = ecdsa.VerifyingKey.from_string(bytes.fromhex(tx['publicKey']), curve=ecdsa.SECP256k1, hashfunc = hashlib.sha1)
                valid = self.util.verifyTransactionRaw(tx, publicKey, 'normal')

                #if(valid == False):
                    #print("TRYING 2")
                    #publicKey = ecdsa.VerifyingKey.from_string(bytes.fromhex(tx['publicKey']), curve=ecdsa.SECP256k1, hashfunc = hashlib.sha1)
                    #valid = self.util.verifyTransactionRaw(tx, publicKey, 'mobile')

                madeWalletAddr, wif = SignaturesECDSA().make_address(publicKey.to_string())
                getOwnWalletFunc = tx['sender']
                if(madeWalletAddr == getOwnWalletFunc):
                    userCurrentBalance, duplicateTx = self.getUserBalance(getOwnWalletFunc, currentBlock, tx['transactionID'], False, True)
                    if(duplicateTx == False):
                        if(userCurrentBalance >= tx['amount']):
                            if(valid):
                                if(tx['recipient'] != tx['sender']):
                                    # Transaction is fully processed and is good to go
                                    execute = True
            else:
                if(tx['sender'] == "genesis"):
                    if(tx['recipient'] == 'LC14NiTUSVd8FJbowK7G8g7yp3HwouNXkr8h'):
                        execute = True
                elif(tx['sender'] == 'validator_reward'): #TODO: take care of this
                    execute = True
            return execute
        except Exception as e:
            print("Error with verifying transaction: " + str(e))
            return False

    def get_current_block_length(self):
        return self.db.Blockchain.estimated_document_count()
    
    def get_previous_block(self, currentHeight):
        docs = self.db.Blockchain.find({"block_height": currentHeight - 1 })
        block = None
        for doc in docs:
            block = doc
        return block

    def new_block(self, VALIDATOR_PEERS, previous_hash=None):

        try:
            lastBlockHash = ''
            currentHeight = self.get_current_block_length()
            #print("Current height: " + str(currentHeight))
            if(currentHeight == 0): # Genesis block
                lastBlockHash = ''
            else:
                previousBlock = self.get_previous_block(currentHeight)
                #print(previousBlock)
                del previousBlock['_id']
                lastBlockHash = self.computeHash(previousBlock)
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
            txThreshold = self.getBlockTXThreshold()
            self.sortTxMempool() # Sorts the mempool by asending order of timestamps
            block = {
                'block_height': currentHeight,
                'timestamp': self.current_transactions_mempool[0:txThreshold][-1]['timestamp'], # TEMPORARY: Timestamp of last transaction is common block timestamp
                'transactions': self.current_transactions_mempool[0:txThreshold], 
                'previous_block': lastBlockHash,
            }
            #print(txThreshold)
            #print( self.current_transactions_mempool)
            #print(block['transactions'])
            
            # Deletes transactions from current mempool
            for txDelete in block['transactions']:
                self.current_transactions_mempool.remove(txDelete)
            #print(self.current_transactions_mempool)
            self.saveBlock(block)

            import sys
            from types import ModuleType, FunctionType
            from gc import get_referents

            # Custom objects know their class.
            # Function objects seem to know way too much, including modules.
            # Exclude modules as well.
            BLACKLIST = type, ModuleType, FunctionType


            def getsize(obj):
                """sum size of object & members."""
                if isinstance(obj, BLACKLIST):
                    raise TypeError('getsize() does not take argument of type: '+ str(type(obj)))
                seen_ids = set()
                size = 0
                objects = [obj]
                while objects:
                    need_referents = []
                    for obj in objects:
                        if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                            seen_ids.add(id(obj))
                            size += sys.getsizeof(obj)
                            need_referents.append(obj)
                    objects = get_referents(*need_referents)
                return size

            print("Size of mempool: " + str(getsize(self.current_transactions_mempool))+ " bytes" + " - # of objects: " + str(len(self.current_transactions_mempool)))
        except Exception as e:
            print("Error with adding block to the chain: " + str(e))
    
    def sortTxMempool(self):
        self.current_transactions_mempool = sorted(self.current_transactions_mempool, key = lambda i: i['timestamp'])
        
    def verifyBlockchainIntegrity(self): 
        blocksHeight = self.get_current_block_length()
        bar = Bar('Verifying blockchain integrity', max=blocksHeight)
        valid = True
        start = timeFunc.time()
        try:
            lastHash = None
            for i in range(blocksHeight):
                currentBlock = self.getBlock(i)
                # Verifies transactions inside block
                for tx in currentBlock['transactions']:
                    if(not self.verifyTransactionBlockchainIntegrity(tx, i)):
                        print("Invalid")
                        valid = False
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
            end = timeFunc.time()
            print("Validated the blockchain integrity in: " + str(end - start) + "s")
            #print("Blockchain is "+ str(valid))
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


    def new_transaction(self, sender, recipient, amount, transactionID, timestamp, hashVal, publicKey, signedMsg, metadata, genesisBlock = False):

        #print("Lenght of transactions: " + str(len(self.current_transactions)))
        transactionSuccess = True
        if(genesisBlock):
            self.current_transactions_mempool.append({
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
                'transactionID': transactionID,
                'timestamp': timestamp,
                'hash': '0x0', #TODO: Add hash
                "public": "none",
                "signedMessage": "none",
                'metadata': ''
            })
        else:
            
            if(len(transactionID) == 98):
                invoicesDataFrom = self.db.Blockchain.find({"transactionID": transactionID })
                #print(invoicesDataFrom.documents)
                #print(invoicesDataTo.documents)
                if(invoicesDataFrom):
                    for invoice in invoicesDataFrom:
                        transactionSuccess = False  # Duplicate transaction ID
                        print(colored("[Share Rejected] Transaction ID is duplicated", 'yellow'))
                self.current_transactions_mempool.append({
                    'sender': sender,
                    'recipient': recipient,
                    'amount': amount,
                    'transactionID': transactionID,
                    'timestamp': timestamp,
                    'hash': hashVal,
                    "publicKey": publicKey,
                    "signedMessage": signedMsg,
                    'metadata': str(metadata)
                })
            else:
                print(colored("[Share Rejected] Transaction ID does not match standard format", 'yellow'))
                transactionSuccess = False
            #return self.last_block.index + 1
        return transactionSuccess

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

    def getUserBalance(self, myPublic, blockLimit = None, checkTransactionID=None, mobileGet=False, integrityCheck=False):
        duplicate = False
        transactionsInfo = []
        duplicateCount = 0
        # Checks for duplicate transaction in mempool
        for tx in self.current_transactions_mempool:
            if(tx['transactionID'] == checkTransactionID):
                duplicate = True
        try:
            if(type(myPublic) != str):
                myPublic = myPublic.decode('utf-8')

            #print(myPublic)
            outgoingTx = None 
            incomingTx = None
            if(blockLimit):
                outgoingTx = self.db.Blockchain.find({"$and": [{"transactions.sender": myPublic}, {"block_height": {"$lte": blockLimit}}]})
                incomingTx = self.db.Blockchain.find({"$and": [{"transactions.recipient": myPublic}, {"block_height": {"$lte": blockLimit}}]})
            else:
                outgoingTx = self.db.Blockchain.find({"transactions.sender": myPublic })
                incomingTx = self.db.Blockchain.find({"transactions.recipient": myPublic })
            balance = 0

            ###################################
            # Checks mempool for transactions
            ###################################

            # Checks outgoing transactions

            for outTxBlock in self.current_transactions_mempool:
                if(outTxBlock['sender'] == myPublic):
                    if(outTxBlock['transactionID'] == checkTransactionID):
                        duplicate = True
                        duplicateCount+=1
                    if(mobileGet):
                        dateTimeObj = datetime.datetime.fromtimestamp(outTxBlock['timestamp'])
                        formattedDate = dateTimeObj.strftime('%m/%d/%y %H:%M:%S')
                        transactionsInfo.append({"type" : "outgoing", "amount" : outTxBlock['amount'], "date" : str(formattedDate), "txID": outTxBlock['transactionID'], "to": outTxBlock['recipient'], "from" : outTxBlock['sender'], "height": 'Unconfirmed', 'metadata': outTxBlock['metadata']})
                    try:
                        balance = balance - outTxBlock['amount']
                    except:
                        balance = balance - outTxBlock.amount

            # Checks incoming transactions

            for inTxBlock in self.current_transactions_mempool:
                if(inTxBlock['recipient'] == myPublic):
                    if(inTxBlock['transactionID'] == checkTransactionID):
                        duplicate = True
                        duplicateCount+=1
                    if(mobileGet):
                        dateTimeObj = datetime.datetime.fromtimestamp(inTxBlock['timestamp'])
                        formattedDate = dateTimeObj.strftime('%m/%d/%y %H:%M:%S')
                        transactionsInfo.append({"type" : "incoming", "amount" : inTxBlock['amount'], "date" : str(formattedDate), "txID": inTxBlock['transactionID'], "to": tx['recipient'], "from" : inTxBlock['sender'], "height": 'Unconfirmed', 'metadata': inTxBlock['metadata']})
                    try:
                        balance = balance + inTxBlock['amount']
                    except:
                        balance = balance + inTxBlock.amount

            ######################################
            # Checks blockchain for transactions
            ######################################

            # Checks outgoing transactions

            for outTxBlock in outgoingTx:
                transactions = outTxBlock['transactions']
                for tx in transactions:
                    if(tx['sender'] == myPublic):
                        if(tx['transactionID'] == checkTransactionID):
                            duplicate = True
                            duplicateCount+=1
                        if(mobileGet):
                            dateTimeObj = datetime.datetime.fromtimestamp(tx['timestamp'])
                            formattedDate = dateTimeObj.strftime('%m/%d/%y %H:%M:%S')
                            transactionsInfo.append({"type" : "outgoing", "amount" : tx['amount'], "date" : str(formattedDate), "txID": tx['transactionID'], "to": tx['recipient'], "from" : tx['sender'], "height": outTxBlock['block_height'], 'metadata': tx['metadata']})
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
                            duplicateCount+=1
                        if(mobileGet):
                            dateTimeObj = datetime.datetime.fromtimestamp(tx['timestamp'])
                            formattedDate = dateTimeObj.strftime('%m/%d/%y %H:%M:%S')
                            transactionsInfo.append({"type" : "incoming", "amount" : tx['amount'], "date" : str(formattedDate), "txID": tx['transactionID'], "to": tx['recipient'], "from" : tx['sender'], "height": incomingTxBlock['block_height'], 'metadata': tx['metadata']})
                        try:
                            balance = balance + tx['amount']
                        except:
                            balance = balance + tx.amount
            
            #print("BALANCE: " + str(balance))

            if(integrityCheck):
                if(duplicateCount <= 1):
                    duplicate = False
            if(mobileGet):
                return balance, duplicate, transactionsInfo
            else:
                return balance, duplicate
                
        except Exception as e:
            print(colored("[FATAL ERROR] Error with fetching user balance: " + str(e), "red"))
            print(traceback.format_exc())

    ####################
    # Invoice support
    ####################

    def create_invoice(self, invoiceID, amount, fromAddr, toAddr, expDate, signature, public, mobile=False):

        #publicKey = ecdsa.VerifyingKey.from_string(bytes.fromhex(public), curve=ecdsa.SECP256k1, hashfunc=sha256)

        #print(publicKey)

        #print(invoiceID)

        originalMessage = str(invoiceID) #+ str(amount) + str(fromAddr) + str(toAddr) + str(expDate) + str(public)

        print(originalMessage)
        print(signature)
        #str(invoiceID) + str(amount) + str(walletAddress) + str(toAddr) + str(expDate) + str(myVerifyingKey.to_string().hex())

        #print(originalMessage)

        #print(bytes(originalMessage, 'utf-8'))

        #print(bytes.fromhex(signature))

        #print(signature)

        #print( bytes.fromhex(signature))

        # print


        #print("DATA: " + str(originalMessage.encode('utf-8')))

        #print("SIGNATURE: " + str(bytes.fromhex(signature)))

        invoiceValid = False

        # Verifies invoice signature

        try:
            
            if(mobile):
                publicUse = ecdsa.VerifyingKey.from_string(bytes.fromhex(public), curve=ecdsa.SECP256k1, hashfunc=sha256) 
            else: pickle.loads(public)


            invoiceValid = SignaturesECDSA().verify(originalMessage.encode('utf-8'), bytes.fromhex(signature), publicUse) 
        
        except:
            pass


        if(invoiceValid):

            if(fromAddr != toAddr):

                if(len(invoiceID) == 85):

                    status = "valid"

                    if(expDate != 'none'):

                        expDateTime = datetime.datetime.fromtimestamp(expDate)
                        expTimstampUTC = expDateTime.replace(tzinfo=datetime.timezone.utc)

                        status = "valid" if(datetime.datetime.now(datetime.timezone.utc).timestamp() < expTimstampUTC.timestamp()) else "invalid"


                    invoicesData = self.db.InvoicePool.find({"invoiceID": invoiceID })

                    duplicate = False

                    # Checks for duplicates

                    if(invoicesData):
                        for invoice in invoicesData:
                            duplicate = True

                    if(not duplicate):
                        invoiceDetails = {
                            "invoiceID": invoiceID,
                            "amount": amount,
                            "fromAddr": fromAddr, 
                            "toAddr": toAddr,
                            "expTimestamp": expDate, 
                            "status": status,
                        }

                        self.db.InvoicePool.insert(invoiceDetails)
                    
                    else:
                        print(colored("[INVOICE REJECTED] Invoice id is duplicated", "red"))
                else:
                    print(colored("[INVOICE REJECTED] Invoice id formatted incorrectly", "red"))


            else:
                print(colored("[INVOICE REJECTED] Cannot send invoice to themself", "red"))
        
        else:
            print("[INVOICE REJECTED] Invoice signature is invalid")
    
    def get_invoices(self, fromAddr, pendingIncoming=True):
        

        fromAddr = fromAddr.decode('utf-8')

        #print(fromAddr)
        invoices = []

        invoicesDataFrom = self.db.InvoicePool.find({"fromAddr": fromAddr })

        #print(invoicesDataFrom.documents)
        #print(invoicesDataTo.documents)

        if(pendingIncoming):
            for invoice in invoicesDataFrom:
                #print(invoice)
                invoices.append(invoice)
        

        
        invoicesDataTo = self.db.InvoicePool.find({"toAddr": fromAddr })
        
        for invoice in invoicesDataTo:
            invoices.append(invoice)
        
        #print(invoices)
        
        return invoices

    def remove_invoice_from_pool(self, invoiceID, senderAddr, ownAddr):
        invoicesFiltered = []
        removedOneInvoice = False
        #print("Removing invoice")
        #print(ownAddr)
        invoicesData = self.db.InvoicePool.find({"invoiceID": invoiceID})
        
        for invoice in invoicesData:
            #print(invoice)
            if(invoice['invoiceID'] == invoiceID and invoice['toAddr'] == ownAddr[0] and invoice['fromAddr'] == senderAddr):
                invoicesFiltered.append(invoice)
            
            else:
                print("NOT EQUAL")

        for invoice in invoicesFiltered:
            try:
                self.db.InvoicePool.delete_one({"invoiceID": invoiceID})
                removedOneInvoice = True
            
            except Exception as e:
                print("Failed to delete one invoice: " + str(e))
        
        return removedOneInvoice
    
    def get_invoices_count():
        try:
            client = MongoClient('localhost')
            db=client.LunarCoin
            data = db.InvoicePool.estimated_document_count()
            return data
        except: return None
    
    def delete_invoice_pool():
        client = MongoClient('localhost')
        db=client.LunarCoin
        db.InvoicePool.delete_many({})

    def save_invoice_chunk(invoices):
        try:
            client = MongoClient('localhost')
            db=client.LunarCoin

            db.InvoicePool.insert_many(invoices)
            
        except Exception as e:
            print("Failed to save invoice chunk")

    def get_invoices_sync_util(page_size, last_id=None):
        try:
            client = MongoClient('localhost')
            db=client.LunarCoin

            if last_id is None:
                # When it is first page
                cursor = db['InvoicePool'].find().limit(page_size)
            else:
                cursor = db['InvoicePool'].find({'_id': {'$gt': last_id}}).limit(page_size)

            # Get the data      
            data = [x for x in cursor]

            if not data:
                # No documents left
                return None, None

            # Since documents are naturally ordered with _id, last document will
            # have max id.
            last_id = data[-1]['_id']

            # Return data and last_id
            return data, last_id
            
        except: return None, None
            








        


        
