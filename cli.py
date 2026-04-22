import argparse
import json
import os
import sys

from bot.client import BinanceClient
from bot.logging_config import get_logger
from bot.orders import OrderManager

logger = get_logger("cli")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Place orders on Binance Futures Testnet (USDT-M)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview order without placing it")
    parser.add_argument("--symbol",     required=True,  help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side",       required=True,  help="BUY or SELL")
    parser.add_argument("--type",       required=True,  dest="order_type", help="MARKET, LIMIT, or STOP_MARKET")
    parser.add_argument("--quantity",   required=True,  help="Order quantity (base asset)")
    parser.add_argument("--price",      default=None,   help="Limit price (required for LIMIT orders)")
    parser.add_argument("--stop-price", default=None,   dest="stop_price", help="Stop price (required for STOP_MARKET)")
    return parser


def print_order_summary(args: argparse.Namespace) -> None:
    print("\n--- Order Request ----------------------------")
    print(f"  Symbol    : {args.symbol.upper()}")
    print(f"  Side      : {args.side.upper()}")
    print(f"  Type      : {args.order_type.upper()}")
    print(f"  Quantity  : {args.quantity}")
    if args.price:
        print(f"  Price     : {args.price}")
    if args.stop_price:
        print(f"  Stop Price: {args.stop_price}")
    print("----------------------------------------------\n")


def print_order_result(result: dict) -> None:
    print("--- Order Response -----------------------------")
    print(f"  Order ID     : {result.get('orderId', 'N/A')}")
    print(f"  Status       : {result.get('status', 'N/A')}")
    print(f"  Executed Qty : {result.get('executedQty', '0')}")
    avg_price = result.get("avgPrice") or result.get("price", "N/A")
    print(f"  Avg Price    : {avg_price}")
    print(f"  Symbol       : {result.get('symbol', 'N/A')}")
    print(f"  Side         : {result.get('side', 'N/A')}")
    print(f"  Type         : {result.get('type', 'N/A')}")
    print("------------------------------------------------")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    api_key    = os.environ.get("BINANCE_API_KEY", "").strip()
    api_secret = os.environ.get("BINANCE_API_SECRET", "").strip()

    if not api_key or not api_secret:
        print(
            "ERROR: Missing API credentials.\n"
            "Set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.\n"
            "Example:\n"
            "  export BINANCE_API_KEY=your_key\n"
            "  export BINANCE_API_SECRET=your_secret"
        )
        sys.exit(1)

    print_order_summary(args)
    if args.dry_run:
        print("Dry run mode — order not placed.\n")
        sys.exit(0)

    client = BinanceClient(api_key, api_secret)
    manager = OrderManager(client)

    try:
        result = manager.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
        )
        print_order_result(result)
        print("\n Order placed successfully.\n")
        logger.info("Full response: %s", json.dumps(result))

    except ValueError as exc:
        print(f"\n Validation error: {exc}\n")
        logger.warning("Validation error: %s", exc)
        sys.exit(2)

    except (ConnectionError, TimeoutError) as exc:
        print(f"\n Network error: {exc}\n")
        logger.error("Network error: %s", exc)
        sys.exit(3)

    except RuntimeError as exc:
        print(f"\n API error: {exc}\n")
        logger.error("API error: %s", exc)
        sys.exit(4)

    except Exception as exc:
        print(f"\n Unexpected error: {exc}\n")
        logger.exception("Unexpected error: %s", exc)
        sys.exit(5)


if __name__ == "__main__":
    main()
