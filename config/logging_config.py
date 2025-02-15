import logging
import logging.handlers
import os
from pathlib import Path
from datetime import datetime

def setup_logging(
    log_level: str = "INFO",
    log_dir: str = "logs",
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Configure logging for the trading bot
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory to store log files
        max_file_size: Maximum size of each log file in bytes
        backup_count: Number of backup files to keep
    """
    # Create logs directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s'
    )

    # Get the root logger
    logger = logging.getLogger("hyperliquid_bot")
    logger.setLevel(log_level)

    # Clear any existing handlers
    logger.handlers.clear()

    # File handler for all logs
    main_log_file = log_path / f"bot_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.handlers.RotatingFileHandler(
        main_log_file,
        maxBytes=max_file_size,
        backupCount=backup_count
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(log_level)
    logger.addHandler(file_handler)

    # Separate file handler for errors
    error_log_file = log_path / f"error_{datetime.now().strftime('%Y%m%d')}.log"
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=max_file_size,
        backupCount=backup_count
    )
    error_handler.setFormatter(file_formatter)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(log_level)
    logger.addHandler(console_handler)

    return logger

# Trading-specific log levels
TRADE_EXECUTED = 25
ORDER_PLACED = 24
POSITION_UPDATED = 23

# Register custom log levels
logging.addLevelName(TRADE_EXECUTED, 'TRADE')
logging.addLevelName(ORDER_PLACED, 'ORDER')
logging.addLevelName(POSITION_UPDATED, 'POSITION')

class TradingLogger(logging.Logger):
    """Extended logger with trading-specific logging methods"""
    
    def trade(self, msg, *args, **kwargs):
        """Log a trade execution"""
        self.log(TRADE_EXECUTED, msg, *args, **kwargs)
    
    def order(self, msg, *args, **kwargs):
        """Log an order placement"""
        self.log(ORDER_PLACED, msg, *args, **kwargs)
    
    def position(self, msg, *args, **kwargs):
        """Log a position update"""
        self.log(POSITION_UPDATED, msg, *args, **kwargs)

# Register the custom logger class
logging.setLoggerClass(TradingLogger)

def get_logger(name: str = "hyperliquid_bot") -> TradingLogger:
    """Get a logger instance with the trading-specific extensions"""
    return logging.getLogger(name)

# Example usage:
if __name__ == "__main__":
    # Setup logging
    setup_logging(log_level="DEBUG")
    logger = get_logger()
    
    # Test various log levels
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
    
    # Test trading-specific logs
    logger.trade("BTC-USDT Long position opened at 50000")
    logger.order("Limit order placed: BTC-USDT @ 49500")
    logger.position("Position size increased to 0.5 BTC")