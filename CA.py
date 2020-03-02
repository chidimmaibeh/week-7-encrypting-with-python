import json
import os


# A method to write down registered servers in a file
# Used by Certificate Authority
def write_json(json_data):
    # Get current working directory
    current_directory = os.getcwd()
    # Now make it an absolute path
    final_directory = os.path.join(current_directory, r'Data')
    # If folder doesn't exist, then make it
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    with open(final_directory + '/servers_registered.json', 'w') as f:
        # Write as json object to file
        json.dump(json_data, f)


# A method to read registered servers from a file
# Used by Certificate Authority
def read_json():
    # Get current working directory
    current_directory = os.getcwd()
    # Now make it an absolute path
    final_directory = os.path.join(current_directory, r'Data')
    # If folder doesn't exist, then make it
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    with open(final_directory + '/servers_registered.json') as f:
        # Read json object from file
        data = json.load(f)
        return data


class CertificateAuthority:

    def __init__(self):
        self.servers_registered = list()

    # This method is used by Certificate Authority to register a server
    def register_server(self, server_name, public_key):
        self.servers_registered.append({
            "server_name": server_name,
            "public_key": public_key.decode()
        })
        write_json(self.servers_registered)

    # This method is used by clients to check if server name provided is valid
    # If server name is valid, this method returns public key, else it returns None
    def validate_server(self, server_name):
        self.servers_registered = read_json()
        for server in self.servers_registered:
            if server_name == server['server_name']:
                return server['public_key'].encode()
        return None
