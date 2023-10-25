import socket
import threading
from time import sleep

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

conns = []
number = 0

def handleConnection(conn, addr):
    global number
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            resp = f"{data.decode('ascii')} | {number}"
            conn.sendall(resp.encode('ascii'))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
      conn, addr = s.accept()
      if conn not in conns:
        conns.append(conn)
        t = threading.Thread(target=handleConnection, args=(conn, addr))
        t.start()
      
      number += 1
      print("Waiting for new connections")
      sleep(1)

    
          

    