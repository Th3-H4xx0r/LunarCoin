import pickle
import sys
import uuid
import base64
import basehash
import zlib


key = b'MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANN/zgMTrkYsV5Lc+ZrXJlWmt1GM+mue\nNupg/CPYQIBoXUi5ftB1kmz85u+7e9iH6lrurwtAGCu7bHTsjD4WGosCAwEAAQ=='

print ("size of original: " + str(len(key)))

compressed = zlib.compress(key)

print("size of compressed: " + str(len(compressed)))

print(compressed)

print(zlib.decompress(compressed))



#id = uuid.UUID(key)

#print(id.int)

#short = base64.b32encode(key)

#print(short)