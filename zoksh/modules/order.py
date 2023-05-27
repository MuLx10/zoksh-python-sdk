from zoksh.modules.api_resource import ApiResource

class ErrorCode:
    INVALID_AMOUNT = "invalid-amount"
    MERCHANT_MISSING = "merchant-order-missing"
    TRANSACTION_MISSING = ""

PATH_CREATE = "/v2/order"

class Order(ApiResource):
    def __init__(self, connector: Connector):
        super().__init__(connector)
        
    def create(self, info):
        if "amount" not in info or not info["amount"]:
            raise ValueError(ErrorCode.INVALID_AMOUNT)
        im = str(info["amount"]).strip()
        if im == "":
            raise ValueError(ErrorCode.INVALID_AMOUNT)
        try:
            am = float(info["amount"])
            if am < 0 or am == float("inf") or am == float("-inf") or am != am:
                raise ValueError(ErrorCode.INVALID_AMOUNT)
        except ValueError:
            raise ValueError(ErrorCode.INVALID_AMOUNT)

        if "merchant" not in info or not info["merchant"]:
            raise ValueError(ErrorCode.MERCHANT_MISSING)
        if "orderId" not in info["merchant"] or not info["merchant"]["orderId"]:
            raise ValueError(ErrorCode.MERCHANT_MISSING)

        return self.connector.signAndSend(PATH_CREATE, info)
