import hashlib
import hmac
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from .logging_config import get_logger

BASE_URL = "https://testnet.binancefuture.com"

logger = get_logger("client")


class BinanceClient:
    

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        })

    

    def _sign(self, params: Dict[str, Any]) -> Dict[str, Any]:
        params["timestamp"] = int(time.time() * 1000)
        query = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _post(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        url = BASE_URL + endpoint
        signed = self._sign(params)
        logger.debug("POST %s  params=%s", url, {k: v for k, v in signed.items() if k != "signature"})
        try:
            resp = self.session.post(url, data=signed, timeout=10)
        except requests.exceptions.ConnectionError as exc:
            logger.error("Network error reaching %s: %s", url, exc)
            raise ConnectionError(f"Could not connect to Binance testnet: {exc}") from exc
        except requests.exceptions.Timeout:
            logger.error("Request to %s timed out", url)
            raise TimeoutError("Request timed out. Check your network connection.")

        logger.debug("Response [%d]: %s", resp.status_code, resp.text)

        if not resp.ok:
            try:
                err = resp.json()
                code = err.get("code", resp.status_code)
                msg = err.get("msg", resp.text)
            except Exception:
                code, msg = resp.status_code, resp.text
            logger.error("API error %s: %s", code, msg)
            raise RuntimeError(f"Binance API error {code}: {msg}")

        return resp.json()

    

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        stop_price: Optional[float] = None,
        time_in_force: str = "GTC",
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            if price is None:
                raise ValueError("Price is required for LIMIT orders.")
            params["price"] = price
            params["timeInForce"] = time_in_force

        elif order_type == "STOP_MARKET":
            if stop_price is None:
                raise ValueError("Stop price is required for STOP_MARKET orders.")
            params["stopPrice"] = stop_price

        return self._post("/fapi/v1/order", params)

    def get_account(self) -> Dict[str, Any]:
        return self._post("/fapi/v2/account", {})
