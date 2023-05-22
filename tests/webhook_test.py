import unittest
from unittest.mock import MagicMock
from zoksh.modules.webhook import Webhook

class WebhookTestCase(unittest.TestCase):
    def setUp(self):
        self.connector = MagicMock()
        self.webhook_endpoint = MagicMock()
        self.webhook = Webhook(self.connector, self.webhook_endpoint)

    def test_parse_valid_request(self):
        headers = {
            "zoksh-key": "zoksh_key",
            "zoksh-ts": "1234567890",
            "zoksh-sign": "signature"
        }
        body = {"amount": "10.0"}
        request = {
            "headers": headers,
            "body": body
        }

        result = self.webhook._parse(request)

        self.assertEqual(result["zokshKey"], "zoksh_key")
        self.assertEqual(result["zokshTs"], "1234567890")
        self.assertEqual(result["zokshSign"], "signature")
        self.assertEqual(result["body"], body)

    def test_parse_invalid_request_missing_headers(self):
        request = {"body": {"amount": "10.0"}}

        with self.assertRaises(Exception):
            self.webhook._parse(request)

    def test_parse_invalid_request_missing_body(self):
        request = {"headers": {"zoksh-key": "zoksh_key"}}

        with self.assertRaises(Exception):
            self.webhook._parse(request)

    def test_test_valid_request(self):
        headers = {
            "zoksh-key": "zoksh_key",
            "zoksh-ts": "1234567890",
            "zoksh-sign": "signature"
        }
        body = {"amount": "10.0"}
        request = {
            "headers": headers,
            "body": body
        }
        self.connector.calculateSignature = MagicMock(return_value={"signature": "signature"})

        result = self.webhook.test(request)

        self.assertTrue(result)
        self.connector.calculateSignature.assert_called_once_with(self.webhook_endpoint, body, "1234567890")

    def test_test_invalid_request_invalid_signature(self):
        headers = {
            "zoksh-key": "zoksh_key",
            "zoksh-ts": "1234567890",
            "zoksh-sign": "signature"
        }
        body = {"amount": "10.0"}
        request = {
            "headers": headers,
            "body": body
        }
        self.connector.calculateSignature = MagicMock(return_value={"signature": "invalid_signature"})

        with self.assertRaises(Exception):
            self.webhook.test(request)

    def test_handle_valid_request(self):
        headers = {
            "zoksh-key": "zoksh_key",
            "zoksh-ts": "1234567890",
            "zoksh-sign": "signature"
        }
        body = {"amount": "10.0"}

        self.webhook.test = MagicMock(return_value=True)

        result = self.webhook.handle(headers, body)

        self.assertTrue(result)
        self.webhook.test.assert_called_once_with({"headers": headers, "body": body})

    def test_express_valid_request(self):
        request = {
            "headers": {
                "zoksh-key": "zoksh_key",
                "zoksh-ts": "1234567890",
                "zoksh-sign": "signature"
            },
            "body": {"amount": "10.0"}
        }

        self.webhook.test = MagicMock(return_value=True)
        next_callback = MagicMock()

        self.webhook.express(request, None, next_callback)

        self.assertTrue(next_callback.called)
        self.webhook.test.assert_called_once_with(request)

if __name__ == '__main__':
    unittest.main()
