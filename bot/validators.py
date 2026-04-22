VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


def validate_symbol(symbol: str) -> str:
    s = symbol.strip().upper()
    if not s.isalnum() or len(s) < 3:
        raise ValueError(f"Invalid symbol '{symbol}'. Expected something like BTCUSDT.")
    return s


def validate_side(side: str) -> str:
    s = side.strip().upper()
    if s not in VALID_SIDES:
        raise ValueError(f"Invalid side '{side}'. Must be one of: {', '.join(VALID_SIDES)}.")
    return s


def validate_order_type(order_type: str) -> str:
    t = order_type.strip().upper()
    if t not in VALID_ORDER_TYPES:
        raise ValueError(
            f"Invalid order type '{order_type}'. Must be one of: {', '.join(VALID_ORDER_TYPES)}."
        )
    return t


def validate_quantity(quantity: str) -> float:
    try:
        q = float(quantity)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid quantity '{quantity}'. Must be a positive number.")
    if q <= 0:
        raise ValueError(f"Quantity must be greater than 0, got {q}.")
    return q


def validate_price(price: str) -> float:
    try:
        p = float(price)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid price '{price}'. Must be a positive number.")
    if p <= 0:
        raise ValueError(f"Price must be greater than 0, got {p}.")
    return p


def validate_stop_price(stop_price: str) -> float:
    return validate_price(stop_price)
