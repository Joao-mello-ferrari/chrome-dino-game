import socket
from time import sleep

class Client(object):
    def __init__(self, host, port):
      self.host = host
      self.port = port
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
    def start(self):
       with self.socket as s:
          s.connect((self.host, self.port))
          while True:

            s.sendall(b"Hello, world")
            data = s.recv(1024)
            if not data:
              print("Timedout")
              break
            print(f"Received {data!r}")
            sleep(1)


c = Client("127.0.0.1", 65432)
c.start()
    
