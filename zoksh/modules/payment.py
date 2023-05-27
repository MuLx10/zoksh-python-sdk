from zoksh.modules.api_resource import ApiResource

class ErrorCode:
    TRANSACTION_MISSING = "transaction-missing"

PATH_VALIDATE = "/v2/validate-payment"

class Payment(ApiResource):
    def __init__(self, connector: Connector):
        super().__init__(connector)
        
    def validate(self, transactionHash):
        if not transactionHash or transactionHash.strip() == "":
            raise ValueError(ErrorCode.TRANSACTION_MISSING)
        
        return self.connector.signAndSend(PATH_VALIDATE, {
            'transaction': transactionHash
        })
