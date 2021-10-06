import pickle
import hashlib


x = {"_id":{"$oid":"615ced8bd014dd92d33cbbbf"},"block_height":1,"timestamp":1633480075.5829105,"transactions":[{"sender":"LC14NiTUSVd8FJbowK7G8g7yp3HwouNXkr8h","recipient":"LC19wZGPX7zUeaL5gvHgT9RduKmJk7JPVzxH","amount":10,"transactionID":"MHgzNDQ3MGFjZThmMGQ0MjY3ZTZjMWVjYjgwNTI1ZTRkMDFlMjgxODk3NmQyYjcyZDM1MzgzODRmOWFiN2Q3MmI4NzhlZGY5MGM1N2RmNDU5ZmMxMjM2ODY5MWViY2YxZWE=","timestamp":1633480070.528882,"hash":'x'}]}
x = pickle.dumps(x)
print(x)


result = hashlib.sha256(x)
print(result.hexdigest())