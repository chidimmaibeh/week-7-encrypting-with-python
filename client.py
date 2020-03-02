import socket

from cipher import Cipher
from CA import CertificateAuthority


class Client:

    def __init__(self, host, port):
        self.socket = socket.socket()
        self.host = host
        self.port = port

    def getConnection(self):
        self.socket.connect((self.host, self.port))

    def endConnection(self):
        # Inform server
        client.sendMessage('shutting_down')
        self.socket.close()

    def recieveMessage(self):
        data = self.socket.recv(1024)
        return data.decode()

    def sendMessage(self, message):
        self.socket.sendall(message.encode())


if __name__ == "__main__":

    # Initialize a client object. 
    client = Client(host=socket.gethostname(), port=443)

    print("[Client] Host: ", client.host)
    print("[Client] Port: ", client.port)

    # initialize connection to the server
    client.getConnection()

    # Ask for server name
    client.sendMessage('get_server_name')

    # receive a response from the server
    server_name = client.recieveMessage()

    # Check if it is a valid server from Certificate Authority
    certificate_authority = CertificateAuthority()
    public_key = certificate_authority.validate_server(server_name)

    # Check if we got servers public key from certificate authority
    if public_key:
        # We got public key of server. Now we will send
        # a message encrypted with servers public key
        encryptor = Cipher(public_key)
        encrypted_data = encryptor.encrypt("session cipher key")

        # Send the encrypted message to server
        client.sendMessage(encrypted_data.decode())

        # receive acknowledgment from server
        server_response = client.recieveMessage()

        # Decrypt the server response to get acknowledgment message
        server_acknowledgment = encryptor.decrypt(server_response).decode()
        print("[Client] Server Acknowledgment message: " + server_acknowledgment)

        # Check if valid acknowledgment is provided by the server
        if server_acknowledgment == 'session cipher key acknowledgement':
            # Now begin transferring of data to server
            data_message = input("Please enter your message for server: ")
            client.sendMessage(encryptor.encrypt(data_message).decode())
            # receive acknowledgment from server
            server_response = client.recieveMessage()

    else:
        print("[Client] Server name wasn't verified from Certificate Authority")
        # Send Goodbye to server
        client.sendMessage('Good Bye')
        # receive acknowledgment from server
        server_response = client.recieveMessage()

    client.endConnection()
