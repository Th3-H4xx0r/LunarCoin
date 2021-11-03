from pymongo import MongoClient

client = MongoClient('localhost')
db=client.LunarCoin




data = db.Blockchain.find({'block_height': 1000})

for block in data:
    #print("BLOCK:" + str(block))
    
    print(block)


