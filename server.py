import socket 

class Server:

    #initialize a Server object
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 9500
        self.socket.bind((self.host, self.port))

    #sends an encoded message over TCP connnection
    def _sendMessage(self, conn, message):
        conn.send(message.encode())
    
    #listening for incoming connections
    def listen(self, printMesage=True):
        self.socket.listen(5)
        if printMesage:
            print('Server is Listening new Connection on Port : ', self.port)
        self._acceptConnecton() 

    #accepts the TCP connections and keeps it alive
    def _acceptConnecton(self):
        print("server to accept the new connection")
        conn, addr = self.socket.accept()
        with conn:
            while True:
                # always listen for incoming messages.
                data = conn.recv(1024)
                if data == b'Hello':
                    self._sendMessage(conn, 'Hi')
                else:
                    self._sendMessage(conn, 'Goodbye')
                    self.listen(False)

 
if __name__ == "__main__":
    #initialize the Server object and starts listening for connections 
    server1 = Server()
    server1.listen()

