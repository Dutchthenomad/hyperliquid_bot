from decimal import Decimal
from typing import Union, Dict, Any, Optional
import re

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

def validate_symbol(symbol: str) -> str:
    """
    Validate trading pair symbol
    
    Args:
        symbol: Trading pair symbol (e.g., "BTC-USDT")
        
    Returns:
        Validated symbol string
        
    Raises:
        ValidationError: If symbol format is invalid
    """
    # Basic symbol format validation
    if not isinstance(symbol, str):
        raise ValidationError("Symbol must be a string")
    
    # Check symbol format (e.g., "BTC-USDT")
    if not re.match(r'^[A-Z0-9]+-[A-Z0-9]+$', symbol):
        raise ValidationError("Invalid symbol format. Expected format: XXX-XXX (e.g., BTC-USDT)")
    
    return symbol

def validate_quantity(
    quantity: Union[str, float, Decimal],
    min_quantity: Optional[Decimal] = None,
    max_quantity: Optional[Decimal] = None
) -> Decimal:
    """
    Validate order quantity
    
    Args:
        quantity: Order quantity
        min_quantity: Minimum allowed quantity
        max_quantity: Maximum allowed quantity
        
    Returns:
        Validated quantity as Decimal
        
    Raises:
        ValidationError: If quantity is invalid
    """
    try:
        quantity_decimal = Decimal(str(quantity))
    except (TypeError, ValueError):
        raise ValidationError("Invalid quantity format")

    if quantity_decimal <= Decimal('0'):
        raise ValidationError("Quantity must be greater than 0")

    if min_quantity and quantity_decimal < min_quantity:
        raise ValidationError(f"Quantity must be at least {min_quantity}")

    if max_quantity and quantity_decimal > max_quantity:
        raise ValidationError(f"Quantity must not exceed {max_quantity}")

    return quantity_decimal

def validate_price(
    price: Union[str, float, Decimal],
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None
) -> Decimal:
    """
    Validate order price
    
    Args:
        price: Order price
        min_price: Minimum allowed price
        max_price: Maximum allowed price
        
    Returns:
        Validated price as Decimal
        
    Raises:
        ValidationError: If price is invalid
    """
    try:
        price_decimal = Decimal(str(price))
    except (TypeError, ValueError):
        raise ValidationError("Invalid price format")

    if price_decimal <= Decimal('0'):
        raise ValidationError("Price must be greater than 0")

    if min_price and price_decimal < min_price:
        raise ValidationError(f"Price must be at least {min_price}")

    if max_price and price_decimal > max_price:
        raise ValidationError(f"Price must not exceed {max_price}")

    return price_decimal

def validate_leverage(leverage: Union[str, int], max_leverage: int = 100) -> int:
    """
    Validate leverage value
    
    Args:
        leverage: Leverage value
        max_leverage: Maximum allowed leverage
        
    Returns:
        Validated leverage as integer
        
    Raises:
        ValidationError: If leverage is invalid
    """
    try:
        leverage_int = int(leverage)
    except (TypeError, ValueError):
        raise ValidationError("Invalid leverage format")

    if leverage_int < 1:
        raise ValidationError("Leverage must be at least 1")

    if leverage_int > max_leverage:
        raise ValidationError(f"Leverage must not exceed {max_leverage}")

    return leverage_int

def validate_order_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate complete order parameters
    
    Args:
        params: Dictionary containing order parameters
        
    Returns:
        Dictionary with validated parameters
        
    Raises:
        ValidationError: If any parameter is invalid
    """
    validated = {}
    
    # Required parameters
    required_params = ['symbol', 'quantity', 'side']
    for param in required_params:
        if param not in params:
            raise ValidationError(f"Missing required parameter: {param}")
    
    # Validate symbol
    validated['symbol'] = validate_symbol(params['symbol'])
    
    # Validate quantity
    validated['quantity'] = validate_quantity(
        params['quantity'],
        min_quantity=params.get('min_quantity'),
        max_quantity=params.get('max_quantity')
    )
    
    # Validate side
    if params['side'] not in ['BUY', 'SELL']:
        raise ValidationError("Invalid side. Must be 'BUY' or 'SELL'")
    validated['side'] = params['side']
    
    # Validate price if present
    if 'price' in params:
        validated['price'] = validate_price(
            params['price'],
            min_price=params.get('min_price'),
            max_price=params.get('max_price')
        )
    
    # Validate leverage if present
    if 'leverage' in params:
        validated['leverage'] = validate_leverage(
            params['leverage'],
            max_leverage=params.get('max_leverage', 100)
        )
    
    # Optional parameters
    optional_params = ['client_order_id', 'time_in_force', 'reduce_only']
    for param in optional_params:
        if param in params:
            validated[param] = params[param]
    
    return validated

def validate_client_order_id(client_order_id: str) -> str:
    """
    Validate client order ID format
    
    Args:
        client_order_id: Client-provided order ID
        
    Returns:
        Validated client order ID
        
    Raises:
        ValidationError: If client order ID is invalid
    """
    if not isinstance(client_order_id, str):
        raise ValidationError("Client order ID must be a string")
    
    if not re.match(r'^[a-zA-Z0-9_-]{1,36}$', client_order_id):
        raise ValidationError(
            "Invalid client order ID format. Must be 1-36 characters long "
            "and contain only letters, numbers, underscore, and hyphen."
        )
    
    return client_order_id