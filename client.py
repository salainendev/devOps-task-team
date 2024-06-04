import socket
import threading
# from hamming_check.hamming import DecodeResult, DecodeStatus, Hamming
# from hamming_check.types.verbosity_types import VerbosityTypes
import time
# hc = hamming = Hamming(1024, VerbosityTypes.QUIET)
alive =True
class Client:
    def __init__(self, name):
        self.name = name
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 5555))
        self.receive_messages_worker = threading.Thread(target=self.receive_messages)
        self.id = None
        self.alive=True
    def register(self):
    

        encoded_data = bytearray(f"ONLINE {self.name}".encode())
        self.client_socket.send(encoded_data)
        response = self.client_socket.recv(1024).decode()
        self.id = response.split()[-1]
        self.receive_messages_worker.start()
        print(f"Registered with ID: {self.id}")
        return 200
    def send_message(self, recipient_name, message):
        
        self.client_socket.send(bytearray(f"SEND {recipient_name} {message}".encode()))
        return 200
    def receive_messages(self):
        while self.alive:
            response = ((self.client_socket.recv(1024))).decode()
            if response:
                with threading.Lock():
                    print("Message received:", response ,'\n')
                    
    def stop(self):
        self.alive = False
        self.client_socket.send(bytearray(f'OFFLINE {self.name}'.encode()))
        self.receive_messages_worker.join()

    def __del__(self):
        self.stop()


if __name__ == "__main__":
    name = input('Welcome to chat by Shaman and Kirushagang, give me ur name: ')
    client = Client(name)
    client.register()
    while True:
        
        name2 = input("write name to who u wanna send message:")
        print('\n')
        message = input('ur message: ')
        print('\n')
        client.send_message(name2, message)