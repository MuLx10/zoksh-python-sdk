import unittest
from unittest.mock import MagicMock
from zoksh.connector import Connector

class ConnectorTestCase(unittest.TestCase):
    def setUp(self):
        self.zoksh_key = "zoksh_key"
        self.zoksh_secret = "zoksh_secret"
        self.connector = Connector(self.zoksh_key, self.zoksh_secret)

    def test_calculate_signature(self):
        path = "/v2/order"
        body = {"amount": "10.0"}

        signature = self.connector.calculateSignature(path, body)

        self.assertIsNotNone(signature["ts"])
        self.assertIsNotNone(signature["signature"])

    def test_sign_and_send(self):
        path = "/v2/order"
        body = {"amount": "10.0"}
        expected_response = {"status": "success"}

        self.connector.doRequest = MagicMock(return_value=expected_response)

        response = self.connector.signAndSend(path, body)

        self.assertEqual(response, expected_response)
        self.connector.doRequest.assert_called_once()

    def test_sign_and_send_with_custom_timestamp(self):
        path = "/v2/order"
        body = {"amount": "10.0"}
        stamp = 1234567890
        expected_response = {"status": "success"}

        self.connector.doRequest = MagicMock(return_value=expected_response)

        response = self.connector.signAndSend(path, body, stamp)

        self.assertEqual(response, expected_response)
        self.connector.doRequest.assert_called_once()

if __name__ == '__main__':
    unittest.main()
