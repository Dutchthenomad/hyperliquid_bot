from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3
import json
from typing import Optional

class WalletManager:
    def __init__(self, private_key: Optional[str] = None):
        """
        Initialize wallet manager.
        
        Args:
            private_key: Optional private key, generates new one if not provided
        """
        if private_key:
            self.account = Account.from_key(private_key)
        else:
            self.account = Account.create()
            
        self.address = self.account.address
        
    def sign_message(self, message: dict) -> str:
        """
        Sign a message with the wallet's private key.
        
        Args:
            message: Message to sign
            
        Returns:
            str: Signature
        """
        message_bytes = Web3.to_bytes(text=json.dumps(message))
        message_hash = encode_defunct(message_bytes)
        signed = self.account.sign_message(message_hash)
        return signed.signature.hex()
