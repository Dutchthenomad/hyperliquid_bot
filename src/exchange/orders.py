from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any
from decimal import Decimal

class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_LOSS = "STOP_LOSS"
    TAKE_PROFIT = "TAKE_PROFIT"

class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStatus(Enum):
    PENDING = "PENDING"
    OPEN = "OPEN"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"

@dataclass
class OrderParams:
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: Decimal
    price: Optional[Decimal] = None  # Required for LIMIT orders
    stop_price: Optional[Decimal] = None  # Required for STOP_LOSS orders
    take_profit_price: Optional[Decimal] = None  # Required for TAKE_PROFIT orders
    leverage: Optional[int] = 1
    time_in_force: str = "GTC"  # Good Till Cancel by default
    reduce_only: bool = False
    client_order_id: Optional[str] = None

@dataclass
class Order:
    params: OrderParams
    status: OrderStatus = OrderStatus.PENDING
    exchange_order_id: Optional[str] = None
    filled_quantity: Decimal = Decimal('0')
    average_fill_price: Optional[Decimal] = None
    last_update_timestamp: Optional[int] = None
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert order to dictionary format for API requests"""
        base_dict = {
            "symbol": self.params.symbol,
            "side": self.params.side.value,
            "orderType": self.params.order_type.value,
            "quantity": str(self.params.quantity),
            "leverage": self.params.leverage,
            "timeInForce": self.params.time_in_force,
            "reduceOnly": self.params.reduce_only
        }

        if self.params.client_order_id:
            base_dict["clientOrderId"] = self.params.client_order_id

        # Add conditional parameters based on order type
        if self.params.order_type == OrderType.LIMIT:
            if not self.params.price:
                raise ValueError("Price is required for LIMIT orders")
            base_dict["price"] = str(self.params.price)

        elif self.params.order_type == OrderType.STOP_LOSS:
            if not self.params.stop_price:
                raise ValueError("Stop price is required for STOP_LOSS orders")
            base_dict["stopPrice"] = str(self.params.stop_price)

        elif self.params.order_type == OrderType.TAKE_PROFIT:
            if not self.params.take_profit_price:
                raise ValueError("Take profit price is required for TAKE_PROFIT orders")
            base_dict["takeProfitPrice"] = str(self.params.take_profit_price)

        return base_dict

    def update_from_exchange(self, exchange_data: Dict[str, Any]) -> None:
        """Update order details from exchange response"""
        self.exchange_order_id = exchange_data.get("orderId")
        self.status = OrderStatus(exchange_data.get("status", "PENDING"))
        
        if "fillQuantity" in exchange_data:
            self.filled_quantity = Decimal(str(exchange_data["fillQuantity"]))
        
        if "averagePrice" in exchange_data:
            self.average_fill_price = Decimal(str(exchange_data["averagePrice"]))
        
        self.last_update_timestamp = exchange_data.get("timestamp")
        self.error_message = exchange_data.get("error")

class OrderManager:
    def __init__(self):
        self.active_orders: Dict[str, Order] = {}
        
    def create_order(self, params: OrderParams) -> Order:
        """Create a new order with given parameters"""
        order = Order(params=params)
        if params.client_order_id:
            self.active_orders[params.client_order_id] = order
        return order
    
    def get_order(self, client_order_id: str) -> Optional[Order]:
        """Retrieve an order by client order ID"""
        return self.active_orders.get(client_order_id)
    
    def update_order(self, client_order_id: str, exchange_data: Dict[str, Any]) -> None:
        """Update an existing order with exchange data"""
        if order := self.active_orders.get(client_order_id):
            order.update_from_exchange(exchange_data)
            
            # Remove filled or cancelled orders from active orders
            if order.status in [OrderStatus.FILLED, OrderStatus.CANCELLED, 
                              OrderStatus.REJECTED, OrderStatus.EXPIRED]:
                self.active_orders.pop(client_order_id, None)
    
    def cancel_order(self, client_order_id: str) -> None:
        """Mark an order as cancelled"""
        if order := self.active_orders.get(client_order_id):
            order.status = OrderStatus.CANCELLED
            self.active_orders.pop(client_order_id, None)

    def get_active_orders(self) -> Dict[str, Order]:
        """Return all active orders"""
        return self.active_orders.copy()
