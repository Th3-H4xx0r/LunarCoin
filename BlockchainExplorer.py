# Imports
import pickle

unser = None
if __name__ == "__main__":
    with open('Blockchain/blockchain.dat', 'rb') as handle:
        unser = pickle.load(handle)
    
        #print(unser)


        chainLength = 0

        print(len(unser))

        index = len(unser) - 1
        currentBlock = unser[index]

        print(unser)


        '''

        while True:
            if(currentBlock.previousBlockHash != ''):
                chainLength = chainLength + 1

                index = index - 1
                currentBlock = currentBlock[index]
            else:
                break

        print(str(chainLength) + " Blocks stored")

        print("Last Block: " + str({'index': unser.index, 'timestamp': unser.timestamp, 'transactions': unser.transactions}))
        '''