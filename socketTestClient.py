import socket               

import time
sock = socket.socket()

host = "10.0.0.30" #ESP32 IP in local network
port = 80          #ESP32 Server Port    

sock.connect((host, port))

while(True):
    x = input("('q' to quit or ('hex' for custom color) or ('rainbow' for rainbow wave) or ('b' for brightness)) >>")
    if(x == 'q'):
        sock.close()
        break

    elif (x == 'hex'):
        r = input("R>")
        g = input("G>")
        b = input("B>")
        sock.send(("RGB:" + str(r) + "-" + str(g) + "*" + str(b)).encode('utf-8'))
    
    elif(x == "b"):
        b = input("Brightness>>")
        sock.send(("BRIGHTNESS:" + str(b)).encode('utf-8'))

    else:
        r,g,b = 0,0,0

        rgbColors = False

        print(x)
        if(x.upper() == "red"):
            r,g,b = 255,000,000
            rgbColors = True
        elif(x.upper() == "green"):
            r,g,b = 000,255,000
            rgbColors = True
        elif(x.upper() == "blue"):
            r,g,b = 000,000,255
            rgbColors = True
        if(rgbColors):
            sock.send(("RGB:" + str(r) + "-" + str(g) + "-" + str(b)).encode('utf-8'))
        else:
            sock.send(x.upper().encode('utf-8'))
        



    





