'''
{
    "minerID": "defaultPranavLaptop1",
    "ngrokAuthToken": "1sbjL6HgcrNZeVi61XPymtYEisD_xaXYnSwRckKbJiUmBfVg",
    "network": "testnet",
    "connection_mode": "ngrok"
}
'''

# Imports
import json
import os

# Global variables
ngrokToken = None


def saveData(data):
    if not os.path.exists('config.json'):
        open('config.json', 'w').close()
    else:
        with open('config.json', 'r+') as f:
            f.seek(0)
            json.dump(data, f)
        


try:
    network = input("Input your network type here (mainnet, testnet, etc)>>")

    while(network == ""):
        print("Input not recognized or is blank. Try again...")
        network = input("Input your network type here (mainnet, testnet, etc)>>")


    minerID = input("Input your minerID here>>")

    while(minerID == ""):
        print("Input not recognized or is blank. Try again...")
        minerID = input("Input your minerID here>>")


    connectionMode = input("Connection mode (tcp or ngork)>>")

    while(connectionMode != "tcp" and connectionMode != "ngrok"):
        print("Input not recognized or is blank. Try again...")
        connectionMode = input("Connection mode (tcp or ngork)>>")

    if(connectionMode == "ngrok"):
        ngrokToken = input("Ngrok token>>")

        while(ngrokToken == ""):
            print("Input not recognized or is blank. Try again...")
            ngrokToken = input("Ngrok token>>")


    data = {
        "minerID": minerID,
        "ngrokAuthToken": ngrokToken,
        "network": network,
        "connection_mode": connectionMode,
    }

    
    try:
        saveData(data)
        print("Setup successful!")
    
    except Exception as f1:
        print("Setup has run into an error: " + str(f1))


except Exception as e:
    print("Setup has run into an error: " + str(e))





