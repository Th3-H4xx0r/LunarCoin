# Imports
import logging
from colorama import init 
from termcolor import colored 

init()

class Logger:

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, filename='runtimeLogger.log', format='%(asctime)s %(levelname)s:%(message)s')

    def logMessage(self, message, level, printMsg=True):

        try:

            if(level == 'warning'):
                logging.warning(message)
                self.printMessage(message, 'yellow', printMsg)

            elif(level == 'info'):
                logging.info(message)
                self.printMessage(message, 'cyan', printMsg)
            
            elif(level == 'success'):
                logging.info(message)
                self.printMessage(message, 'green', printMsg)
            
            elif(level == 'error'):
                logging.error(message)
                self.printMessage(message, 'red', printMsg)

            elif(level == 'regular'):
                logging.info(message)
                self.printMessage(message, None, printMsg)

            elif(level == 'info-blue'):
                logging.info(message)
                self.printMessage(message, 'blue', printMsg)
            
            elif(level == 'info-red'):
                logging.info(message)
                self.printMessage(message, 'red', printMsg)
            
            elif(level == 'info-yellow'):
                logging.info(message)
                self.printMessage(message, 'red', printMsg)

        except Exception as e:
            print("Logging service error: " + str(e))

            

    
    def printMessage(self, message, color, printMsg):

        try:
            if(printMsg):
                if(color == None):
                    print(message)
                else:
                    print(colored(message, color))
        
        except Exception as e:
            print("Logging service print error: " + str(e))
