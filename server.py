import socket

from cryptography.fernet import Fernet
from CA import CertificateAuthority

from cipher import Cipher


class Server:

    # initialize a Server object
    def __init__(self):
        # to use IPv4(AF_INET) and mode of transmission TCP (SOCK_STREAM)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Get hostname of server
        self.host = socket.gethostname()
        self.port = 443
        self.socket.bind((self.host, self.port))
        # Generate a key for server encryption and decryption
        self.public_key = Fernet.generate_key()
        # Get server name
        self.server_name = self.host + str(self.port)
        self.trusted_clients = list()

    # sends an encoded message over TCP connnection
    def _sendMessage(self, conn, message):
        conn.send(message.encode())

    # listening for incoming connections
    def listen(self, printMesage=True):
        self.socket.listen(5)
        if printMesage:
            print('[Server] Server is Listening new Connection on Port : ', self.port)
        self._acceptConnecton()

    def get_client_address(self, addr):
        return addr[0] + ':' + str(addr[1])

    # accepts the TCP connections and keeps it alive
    def _acceptConnecton(self):
        print("[Server] Server to accept the new connection")
        conn, addr = self.socket.accept()
        encryptor = Cipher(self.public_key)
        with conn:
            while True:
                # always listen for incoming messages.
                data = conn.recv(1024)
                # Check if client is asking for server name
                if data == b'get_server_name':
                    # Send servers name to client
                    print("[Server] Sending server name to client")
                    self._sendMessage(conn, self.server_name)
                # Check if client is closing its connection with the server
                elif data == b'shutting_down':
                    # Remove client from trusted list
                    print("[Server] Client closing the connection")
                    self.trusted_clients.remove(self.get_client_address(addr))
                    # Drop connection with current client and start listening for new ones
                    self.listen(False)
                else:
                    # Check if client already has sent valid cipher key and is now transferring data
                    if self.get_client_address(addr) in self.trusted_clients:
                        if data:
                            # Client is transferring data right now
                            print("[Server] Message from client: " + encryptor.decrypt(data.decode()).decode())
                            ack_message = "OK"
                            self._sendMessage(conn, encryptor.encrypt(ack_message).decode())
                    # Lets see if client sent us valid cipher key phrase
                    elif encryptor.decrypt(data.decode()) == b'session cipher key':
                        client_address = self.get_client_address(addr)
                        # Prepare acknowledgment message for client
                        ack_message = "session cipher key acknowledgement"
                        # Mark this client trusted
                        self.trusted_clients.append(client_address)
                        print("[Server] Client sent valid session cipher key")
                        # Send acknowledgment message to client
                        self._sendMessage(conn, encryptor.encrypt(ack_message).decode())

                    else:
                        # Client has provided invalid session cipher key
                        ack_message = "Invalid session cipher key"
                        print("[Server] Client sent invalid session cipher key")
                        self._sendMessage(conn, encryptor.encrypt(ack_message).decode())
                        # Drop connection with current client and start listening for new ones
                        self.listen(False)

    # This method is used by server to register itself with the Certificate Authority
    def register_with_ca(self):
        certificate_authority = CertificateAuthority()
        certificate_authority.register_server(self.server_name, self.public_key)


if __name__ == "__main__":
    # initialize the Server object and starts listening for connections
    server1 = Server()

    # Register the server with Certificate Authority
    server1.register_with_ca()

    # Now listen for connections
    server1.listen()
