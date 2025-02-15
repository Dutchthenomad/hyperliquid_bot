
import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # API Settings
    TESTNET: bool = os.getenv('TESTNET', 'True').lower() == 'true'
    BASE_URL: str = "https://api.testnet.hyperliquid.xyz" if TESTNET else "https://api.hyperliquid.xyz"
    
    # Wallet Settings
    PRIVATE_KEY: str = os.getenv('PRIVATE_KEY', '')
    
    # Trading Settings
    DEFAULT_LEVERAGE: int = 10
    MAX_POSITION_SIZE: float = 1.0
    MIN_SPREAD: float = 0.001  # 0.1%
    
    # Logging Settings
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = 'bot.log'

settings = Settings()