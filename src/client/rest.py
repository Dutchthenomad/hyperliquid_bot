import aiohttp
import time
from typing import Optional, Dict, List, Any
from ..exchange.types import OrderSpec, OrderResponse
from ..utils.auth import WalletManager

class RestClient:
    def __init__(self, base_url: str, wallet_manager: Optional[WalletManager] = None):
        """
        Initialize REST client.
        
        Args:
            base_url: Base API URL
            wallet_manager: Optional wallet manager for signing
        """
        self.base_url = base_url
        self.wallet_manager = wallet_manager
        self.headers = {"Content-Type": "application/json"}
        
    async def _request(self, method: str, endpoint: str, **kwargs) -> Optional[dict]:
        """Make HTTP request to API."""
        url = f"{self.base_url}/{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as response:
                try:
                    response.raise_for_status()
                    return await response.json()
                except aiohttp.ClientError as e:
                    print(f"API request failed: {e}")
                    return None

    def _prepare_action(self, action: dict, vault_address: Optional[str] = None) -> dict:
        """Prepare an action with nonce and signature."""
        if not self.wallet_manager:
            raise ValueError("Wallet manager required for signed requests")
            
        payload = {
            "action": action,
            "nonce": int(time.time() * 1000),
        }
        
        if self.wallet_manager:
            payload["signature"] = self.wallet_manager.sign_message(action)
            
        if vault_address:
            payload["vaultAddress"] = vault_address
            
        return payload
