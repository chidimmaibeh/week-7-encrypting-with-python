import socket

class Client():
    
    def __init__(self, host, port):
        self.socket = socket.socket()
        self.host = host
        self.port = port

    def getConnection(self):
        self.socket.connect((self.host, self.port))
    
    def endConnection(self):
        self.socket.close()

    def recieveMessage(self):
       data = self.socket.recv(1024)
       return data.decode()


    def sendMessage(self, message):
        self.socket.sendall(message.encode())

if __name__ == "__main__":
    # send "Hello" string to the server to receive "Hi" string
    # any other data "Goodbye" string is received from the Server 
    # and ends the connection

    message = input("Input message to send :")

    # Initialize a client object. 
    client = Client(host=socket.gethostname(), port=9500)
    
    print("Host: ", client.host)
    print("Port: ", client.port)

    # initialize connection to the server
    client.getConnection()

    print("sending Message:", message)
    
    #send the encoded message to the server
    client.sendMessage(message)
    
    #receive a response from the server
    receivedMessage = client.recieveMessage()

    print("received Message :", receivedMessage)

    client.endConnection()
 

