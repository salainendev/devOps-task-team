import socket
import threading

import time
id_counter = 0


# это штука это таблица из имён и айдишников для того чтоб перенаправлять сообщения 
class RoutingTable:
    def __init__(self):
        self.users = {}
        self.next_id = 1

    def add_user(self, name):
        if name not in self.users:
            self.users[name] = self.next_id
            self.next_id += 1
        return self.users[name]

    def get_user_id(self, name):
        return self.users.get(name, None)
    

router = RoutingTable()

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('127.0.0.1', 5555))
        self.server_socket.listen(5)
        print("Server started")
        self.clients = {}

    def handle_client(self, client_socket):
        while True:
            try:
                message = (client_socket.recv(1024)).decode()
                if message:
                    self.process_message(client_socket, message)
            except:
                break

    def process_message(self, client_socket, message):
        parts = message.split()
        command = parts[0]
        if command == "OFFLINE":
            self.clients.pop(router.get_user_id(parts[1]))
            print(f"user {parts[1]} left the chat ")
        elif command == "ONLINE":
            print('ONLINE')
            if router.get_user_id(parts[1])==None:
                name = parts[1]
                user_id = router.add_user(name)
                self.clients[user_id] = client_socket
                client_socket.send(bytearray((f"REGISTERED {user_id}".encode())))
            else:
                self.clients[router.get_user_id(parts[1])]=client_socket

                client_socket.send(bytearray((f"WELLCOME your id: {router.get_user_id(parts[1])}".encode())))

        elif command == "SEND":
            recipient_name = parts[1]
            encoded_message = ' '.join(parts[2:])
            recipient_id = router.get_user_id(recipient_name)
            if recipient_id in self.clients:
                self.clients[recipient_id].send(bytearray(encoded_message.encode()))
                client_socket.send((bytearray("Message delivered".encode())))
            else:
                client_socket.send((bytearray("User not registered or not online".encode())))

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            

    def stop(self):
        self.server_socket.close()
        print("server disabled")

    def __del__ (self):
        self.stop()
    
if __name__ == '__main__':
    server = Server()
    server.start()
    server.stop()

def startServ():
    server = Server()
    server.start()
    server.stop()
