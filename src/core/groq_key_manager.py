"""
API Key rotation manager for Groq API
Handles automatic failover when rate limits are hit
"""

from typing import List, Set

from src.utils.config import Config
from src.utils.logger import setup_logger
from src.utils.exceptions import APIError, ConfigurationError

logger = setup_logger(__name__)


class GroqKeyManager:
    """
    Manages API key rotation for Groq
    
    Features:
    - Loads multiple API keys from environment
    - Automatic rotation on rate limit (429) errors
    - Tracks failed keys to avoid retry loops
    - Thread-safe singleton pattern
    
    Example:
        >>> manager = GroqKeyManager()
        >>> current_key = manager.get_current_key()
        >>> if rate_limit_error:
        ...     success = manager.rotate_key()
    """
    
    # Class-level state for singleton pattern
    _all_api_keys: List[str] = []
    _current_key_index: int = 0
    _failed_keys: Set[str] = set()
    _initialized: bool = False
    
    def __init__(self):
        """Initialize API key manager and load keys"""
        if not GroqKeyManager._initialized:
            self._load_keys()
            GroqKeyManager._initialized = True
    
    def _load_keys(self) -> None:
        """
        Load all API keys from configuration
        
        Raises:
            ConfigurationError: If no API keys available
        """
        GroqKeyManager._all_api_keys = Config.get_all_groq_api_keys()
        
        if not GroqKeyManager._all_api_keys:
            logger.warning("No Groq API keys found in configuration")
            return
        
        logger.info(f"Loaded {len(GroqKeyManager._all_api_keys)} Groq API key(s) for rotation")
    
    def get_current_key(self) -> str:
        """
        Get the current active API key
        
        Skips over keys marked as failed and returns the next available key.
        
        Returns:
            Current API key string
            
        Raises:
            APIError: If all keys are exhausted/failed
        """
        if not GroqKeyManager._all_api_keys:
            raise ConfigurationError("No Groq API keys available")
        
        # Skip failed keys
        attempts = 0
        max_attempts = len(GroqKeyManager._all_api_keys)
        
        while attempts < max_attempts:
            key = GroqKeyManager._all_api_keys[GroqKeyManager._current_key_index]
            
            if key not in GroqKeyManager._failed_keys:
                return key
            
            # This key failed, try next one
            GroqKeyManager._current_key_index = (
                (GroqKeyManager._current_key_index + 1) % len(GroqKeyManager._all_api_keys)
            )
            attempts += 1
        
        # All keys have failed
        raise APIError(
            f"All {len(GroqKeyManager._all_api_keys)} Groq API key(s) have been exhausted or rate-limited"
        )
    
    def rotate_key(self) -> bool:
        """
        Rotate to the next available API key
        
        Marks the current key as failed and attempts to switch to the next
        non-failed key. Returns False if all keys have been exhausted.
        
        Returns:
            True if rotation successful, False if all keys exhausted
            
        Example:
            >>> manager = GroqKeyManager()
            >>> if manager.rotate_key():
            ...     print("Successfully rotated to new key")
            ... else:
            ...     print("All keys exhausted")
        """
        if not GroqKeyManager._all_api_keys or len(GroqKeyManager._all_api_keys) <= 1:
            logger.warning("Cannot rotate Groq keys: only one or no API keys available")
            return False
        
        # Mark current key as failed
        current_key = GroqKeyManager._all_api_keys[GroqKeyManager._current_key_index]
        GroqKeyManager._failed_keys.add(current_key)
        logger.debug(f"Marked Groq key {GroqKeyManager._current_key_index + 1} as failed")
        
        # Try next keys
        original_index = GroqKeyManager._current_key_index
        attempts = 0
        
        while attempts < len(GroqKeyManager._all_api_keys):
            GroqKeyManager._current_key_index = (
                (GroqKeyManager._current_key_index + 1) % len(GroqKeyManager._all_api_keys)
            )
            attempts += 1
            
            # Check if we've cycled back to original (all keys tried)
            if GroqKeyManager._current_key_index == original_index:
                logger.error("All Groq API keys have been exhausted")
                return False
            
            # Get next key
            next_key = GroqKeyManager._all_api_keys[GroqKeyManager._current_key_index]
            
            # Skip if already failed
            if next_key in GroqKeyManager._failed_keys:
                continue
            
            # Found a non-failed key
            logger.info(
                f"Rotated to Groq API key {GroqKeyManager._current_key_index + 1}/"
                f"{len(GroqKeyManager._all_api_keys)}"
            )
            return True
        
        # All keys failed
        logger.error("All Groq API keys have been marked as failed")
        return False
    
    def get_key_index(self) -> int:
        """
        Get the current key index (1-based for display)
        
        Returns:
            Current key index (1-based)
        """
        return GroqKeyManager._current_key_index + 1
    
    def get_total_keys(self) -> int:
        """
        Get total number of available keys
        
        Returns:
            Total key count
        """
        return len(GroqKeyManager._all_api_keys)
    
    def reset_failed_keys(self) -> None:
        """
        Reset the failed keys set (useful for testing or daily quota resets)
        
        Warning:
            Use with caution - only call when you know quotas have reset
        """
        logger.info(f"Resetting {len(GroqKeyManager._failed_keys)} failed Groq key(s)")
        GroqKeyManager._failed_keys.clear()
    
    def is_rate_limit_error(self, error: Exception) -> bool:
        """
        Check if an error is a rate limit error
        
        Args:
            error: Exception to check
            
        Returns:
            True if error indicates rate limiting
        """
        error_str = str(error).lower()
        rate_limit_indicators = [
            'quota',
            'rate limit',
            '429',
            'resource_exhausted',
            'too many requests',
            'rate_limit_exceeded'
        ]
        
        return any(indicator in error_str for indicator in rate_limit_indicators)
