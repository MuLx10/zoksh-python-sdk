import unittest
from unittest.mock import MagicMock
from zoksh.modules.order import Order, ErrorCode

class OrderTestCase(unittest.TestCase):
    def setUp(self):
        # Create a mock Connector instance
        self.connector = MagicMock()
        self.order = Order(self.connector)

    def test_create_valid_order(self):
        info = {
            'amount': '10.0',
            'merchant': {
                'orderId': '12345'
            }
        }
        self.connector.signAndSend.return_value = {'orderId': '12345', 'createdAt': 1234567890}

        response = self.order.create(info)

        self.assertEqual(response, {'orderId': '12345', 'createdAt': 1234567890})
        self.connector.signAndSend.assert_called_once_with('/v2/order', info)

    def test_create_invalid_amount(self):
        info = {
            'amount': '',
            'merchant': {
                'orderId': '12345'
            }
        }

        with self.assertRaisesRegex(Exception, ErrorCode.INVALID_AMOUNT):
            self.order.create(info)

    def test_create_missing_merchant(self):
        info = {
            'amount': '10.0'
        }

        with self.assertRaisesRegex(Exception, ErrorCode.MERCHANT_MISSING):
            self.order.create(info)

if __name__ == '__main__':
    unittest.main()
