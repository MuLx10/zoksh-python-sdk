from zoksh.connector import Connector
from zoksh.modules.api_resource import ApiResource

class ErrorCode:
    INVALID_REQUEST = "invalid-request"
    MISSING_REQUEST_HEADERS = "missing-request-headers"
    INVALID_REQUEST_HEADERS = "invalid-request-headers"
    MISSING_REQUEST_BODY = "missing-request-body"
    INVALID_SIGNATURE = "invalid-signature"

class Webhook(ApiResource):
    def __init__(self, connector: Connector, webhookEndPoint: str):
        super().__init__(connector)
        self.endpoint = webhookEndPoint

    def _parse(self, req):
        if not req:
            raise ValueError(ErrorCode.INVALID_REQUEST)
        if not req.get("headers"):
            raise ValueError(ErrorCode.MISSING_REQUEST_HEADERS)
        if not req.get("body"):
            raise ValueError(ErrorCode.MISSING_REQUEST_BODY)
        
        headers = req["headers"]
        zokshKey = headers.get("zoksh-key")
        zokshTs = headers.get("zoksh-ts")
        zokshSign = headers.get("zoksh-sign")
        
        if not zokshKey or not zokshTs or not zokshSign:
            raise ValueError(ErrorCode.INVALID_REQUEST_HEADERS)
        
        body = req["body"]
        return {"zokshKey": zokshKey, "zokshTs": zokshTs, "zokshSign": zokshSign, "body": body}

    def test(self, req):
        parsed_data = self._parse(req)
        zokshSign = parsed_data["zokshSign"]
        zokshTs = parsed_data["zokshTs"]
        body = parsed_data["body"]

        calculated = self.connector.calculateSignature(self.endpoint, body, zokshTs)
        signature = calculated["signature"]
        if signature != zokshSign:
            raise ValueError(ErrorCode.INVALID_SIGNATURE)
        return True

    def handle(self, headers, body):
        return self.test({"headers": headers, "body": body})

    def express(self, req, res, next):
        try:
            self.test(req)
            next(True)
        except Exception as e:
            if next:
                next(e)
