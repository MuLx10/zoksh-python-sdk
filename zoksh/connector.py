import http.client
import json
import time
import hashlib
from urllib.parse import urlparse

SANDBOX_NETWORK_PATH = "payments.sandbox.zoksh.com"
PROD_NETWORK_PATH = "payments.zoksh.com"

class Connector:
    def __init__(self, zokshKey, zokshSecret, sandbox=True):
        self.zokshKey = zokshKey
        self.zokshSecret = zokshSecret
        self.basePath = SANDBOX_NETWORK_PATH if sandbox else PROD_NETWORK_PATH

    def calculateSignature(self, path, body, useTime=-1):
        postBody = json.dumps(body)
        ts = useTime if useTime != -1 else int(time.time() * 1000)
        hmac = hashlib.sha256(bytes(self.zokshSecret, "utf-8"))

        toSign = str(ts) + path + postBody
        hmac.update(bytes(toSign, "utf-8"))
        signature = hmac.hexdigest()
        return {"ts": ts, "signature": signature}

    def doRequest(self, options, data, resolve, reject):
        conn = http.client.HTTPSConnection(options["hostname"])

        conn.request("POST", options["path"], body=data, headers=options["headers"])
        res = conn.getresponse()

        if res.status == 301 or res.status == 302:
            if self.redirectCount < 3:
                self.redirectCount += 1
                loc = res.getheader("location")
                url = urlparse(loc)
                opts = {
                    "method": "POST",
                    "hostname": url.hostname,
                    "path": url.path,
                    "headers": options["headers"],
                }
                self.doRequest(opts, data, resolve, reject)
                return
            else:
                raise ValueError("Server redirected too many times")

        d = res.read().decode("utf-8")
        try:
            return json.loads(d)
        except Exception as e:
            return (e)

    def signAndSend(self, path, body, stamp=-1):
        calculated = self.calculateSignature(path, body, stamp)
        ts = calculated["ts"]
        signature = calculated["signature"]
        data = json.dumps(body).encode("utf-8")
        options = {
            "method": "POST",
            "hostname": self.basePath,
            "path": path,
            "headers": {
                "Content-Type": "application/json",
                "Content-Length": len(data),
                "ZOKSH-KEY": self.zokshKey,
                "ZOKSH-TS": str(ts),
                "ZOKSH-SIGN": signature,
            },
        }

        return self.doRequest(options, data)