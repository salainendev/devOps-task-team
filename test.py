import unittest
import threading
import time
from server import Server
from client import Client
from server import startServ
class TestChat(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server_thread = threading.Thread(target=startServ, daemon=True)
        cls.server_thread.start()
        time.sleep(1)  # Подождем, пока сервер запустится

    def setUp(self):
        self.client1 = Client('test')

    def tearDown(self):
        self.client1.stop()

    def test_registration(self):
        response = self.client1.register()
        self.assertEqual(response,200)
        response = self.client1.send_message("user2", "Hello, user2!")
        self.assertEqual(response, 200)
        
    

if __name__ == '__main__':
    unittest.main()
