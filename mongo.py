from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
import time 
import math
import sys
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string



client = MongoClient('localhost')
db=client.LunarCoin

# Issue the serverStatus command and print the results
#serverStatusResult=db.command("serverStatus")
#pprint(serverStatusResult)

ticTotal = time.perf_counter()


transactionsSim = 100

for i in range(transactionsSim):
    exe = False

    def convert_size(size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])


    txs = []

    blocks = []

    for i in range(1):
        txs.append({"wallet": "newTx1", 'amount': 1, 'timestamp': 10001010101})

    for i in range(199):
        txs.append({"wallet": "randoma", 'amount': 1, 'timestamp': 10001010101})

    if exe:
        for i in range(5):
            block = {
                "block": i,
                "tx": txs
            }

            blocks.append(block)




        db.Transactions.insert_many(blocks)



    tic = time.perf_counter()

        #if(i % 1000 == 0):
    docs = db.Transactions.find({"tx.wallet": 'newTx1' })


    totalTx = 0

    totalTx = 0

    x = 1
    for doc in docs:
        #print(doc)
        if(x == 1):
            #print(doc)
            pass
        #print("Size of block: " + str(convert_size(sys.getsizeof(docs))))
        for transaction in doc['tx']:
            if(transaction['wallet'] == 'newTx1'):
                totalTx = totalTx + transaction['amount']
                totalTx = totalTx + 1
        
        x = x + 1

    #print("TOTAL TX MADE: $" + str(totalTx) + " Total Transactions: " + str(totalTx))
    #print(db.Transactions.estimated_document_count()) 

    toc = time.perf_counter()

    print(f" read in {toc - tic:0.4f} seconds")


tocTotal = time.perf_counter()

timeSpent = tocTotal - ticTotal

print(f" read in {timeSpent} seconds")

print(str(transactionsSim/timeSpent) + " tx/s")