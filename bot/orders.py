from typing import Optional

from .client import BinanceClient
from .logging_config import get_logger
from .validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_stop_price,
    validate_symbol,
)

logger = get_logger("orders")


class OrderManager:
    def __init__(self, client: BinanceClient):
        self.client = client

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: str,
        price: Optional[str] = None,
        stop_price: Optional[str] = None,
    ) -> dict:
        # Validate all inputs up front
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        order_type = validate_order_type(order_type)
        qty = validate_quantity(quantity)

        parsed_price: Optional[float] = None
        parsed_stop: Optional[float] = None

        if order_type == "LIMIT":
            if price is None:
                raise ValueError("--price is required for LIMIT orders.")
            parsed_price = validate_price(price)

        if order_type == "STOP_MARKET":
            if stop_price is None:
                raise ValueError("--stop-price is required for STOP_MARKET orders.")
            parsed_stop = validate_stop_price(stop_price)

        logger.info(
            "Placing %s %s order | symbol=%s qty=%s price=%s stop=%s",
            side, order_type, symbol, qty, parsed_price, parsed_stop,
        )

        result = self.client.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=qty,
            price=parsed_price,
            stop_price=parsed_stop,
        )

        logger.info("Order placed successfully | orderId=%s status=%s", result.get("orderId"), result.get("status"))
        return result
