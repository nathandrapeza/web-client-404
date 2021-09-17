#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():

    #create socket, bind, and set to listening mode
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #allow reused addresses
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(2)

        while True:
            #accept connections and start a Process daemon for handling multiple connections
            conn, addr = s.accept()
            p = Process(target=handle_echo, args=(addr,conn))
            p.daemon = True
            p.start()
            print("Started process ", p)

#echo conncetions back to client
def handle_echo(addr, conn):
    print("Connected by", addr)

    full_data = conn.recv(BUFFER_SIZE)
    conn.sendall(full_data)
    try:
        conn.shutdown(socket.SHUT_RDWR) # this line was causing a bunch of problems
    except:
        pass
    conn.close()

if __name__ == "__main__":
    main()
