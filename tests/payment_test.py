import unittest
from unittest.mock import MagicMock
from zoksh.modules.payment import Payment, ErrorCode

class PaymentTestCase(unittest.TestCase):
    def setUp(self):
        # Create a mock Connector instance
        self.connector = MagicMock()
        self.payment = Payment(self.connector)

    def test_validate_valid_transaction(self):
        transaction_hash = 'abcd1234'
        self.connector.signAndSend.return_value = {'status': 'success'}

        response = self.payment.validate(transaction_hash)

        self.assertEqual(response, {'status': 'success'})
        self.connector.signAndSend.assert_called_once_with('/v2/validate-payment', {'transaction': transaction_hash})

    def test_validate_missing_transaction(self):
        transaction_hash = ''

        with self.assertRaisesRegex(Exception, ErrorCode.TRANSACTION_MISSING):
            self.payment.validate(transaction_hash)


if __name__ == '__main__':
    unittest.main()
