from zoksh.connector import Connector

class ApiResource:
    def __init__(self, conn: Connector):
        self.connector = conn
