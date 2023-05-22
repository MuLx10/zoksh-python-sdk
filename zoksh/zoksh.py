from urllib.parse import urlparse
from zoksh.connector import Connector
from zoksh.modules.order import Order
from zoksh.modules.payment import Payment
from zoksh.modules.webhook import Webhook

PATHS = {
    'ORDER_CREATE': '/v2/order',
    'VALIDATE_PAYMENT': '/v2/validate-payment',
}

class Zoksh:
    def __init__(self, zokshKey, zokshSecret, testnet=True):
        if not zokshKey:
            raise ValueError("Zoksh key missing")
        if not zokshSecret:
            raise ValueError("Zoksh secret missing")
        
        self.connector = Connector(zokshKey, zokshSecret, testnet)
        self._order = Order(self.connector)
        self._payment = Payment(self.connector)
        self._webhook = None

    @property
    def order(self):
        return self._order

    @property
    def payment(self):
        return self._payment

    @property
    def webhookEndPoint(self):
        return self._webhook

    @webhookEndPoint.setter
    def webhookEndPoint(self, url):
        try:
            parsed = urlparse(url)
            if not self._webhook:
                self._webhook = Webhook(self.connector, parsed)
        except Exception as e:
            raise e

    @property
    def webhook(self):
        if not self._webhook:
            raise ValueError("Webhook end point not defined, please call zoksh.webhookEndPoint() first")
        return self._webhook

    def createOrder(self, body):
        return self.connector.signAndSend(PATHS['ORDER_CREATE'], body)

    def validatePayment(self, transactionHash):
        return self.connector.signAndSend(PATHS['VALIDATE_PAYMENT'], {
            'transaction': transactionHash
        })
