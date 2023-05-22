import unittest
from unittest.mock import MagicMock
from zoksh.zoksh import *

class ZokshTestCase(unittest.TestCase):
    def setUp(self):
        # Create a mock Connector instance
        self.connector = MagicMock()
        self.zoksh = Zoksh("zoksh_key", "zoksh_secret", testnet=True)
        self.zoksh.connector = self.connector

    def test_create_order(self):
        info = {'amount': '10.0'}
        self.connector.signAndSend.return_value = {'orderId': '12345', 'createdAt': 1234567890}

        response = self.zoksh.createOrder(info)

        self.assertEqual(response, {'orderId': '12345', 'createdAt': 1234567890})
        self.connector.signAndSend.assert_called_once_with('/v2/order', info)

    def test_validate_payment(self):
        transaction_hash = 'abcd1234'
        self.connector.signAndSend.return_value = {'status': 'success'}

        response = self.zoksh.validatePayment(transaction_hash)

        self.assertEqual(response, {'status': 'success'})
        self.connector.signAndSend.assert_called_once_with('/v2/validate-payment', {'transaction': transaction_hash})


if __name__ == '__main__':
    unittest.main()
