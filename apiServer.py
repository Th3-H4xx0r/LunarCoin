# Imports
from flask import Flask
from flask import request
import pickle
from pyngrok import ngrok
import threading

app = Flask(__name__)

@app.route("/")
def index():
    return "Server cannot handle your request"


@app.route("/blockchain/")
def balance():

    with open('blockchain.dat', 'rb') as handle:
            return str(pickle.load(handle))
  

def runApp():


    app.run(host = '0.0.0.0', port=4993, debug=True)


if __name__ == "__main__":
    runApp()
    

    


