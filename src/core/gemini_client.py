"""
Google Gemini AI client with automatic model detection
Handles connection management and model selection
"""

from typing import Optional
import google.generativeai as genai

from src.core.api_key_manager import APIKeyManager
from src.utils.logger import setup_logger
from src.utils.exceptions import APIError

logger = setup_logger(__name__)


class GeminiClient:
    """
    Wrapper for Google Gemini AI client
    
    Features:
    - Automatic best model detection
    - Connection management with retry logic
    - Integration with APIKeyManager for rotation
    
    Example:
        >>> client = GeminiClient()
        >>> model = client.get_model()
        >>> response = model.generate_content("SELECT * FROM users")
    """
    
    def __init__(self, api_key_manager: Optional[APIKeyManager] = None):
        """
        Initialize Gemini client
        
        Args:
            api_key_manager: Optional APIKeyManager instance. Creates new if None.
            
        Raises:
            APIError: If cannot connect to Gemini API
        """
        self.api_key_manager = api_key_manager or APIKeyManager()
        self.model_name: Optional[str] = None
        self.model: Optional[genai.GenerativeModel] = None
        
        self._initialize()
    
    def _initialize(self) -> None:
        """
        Initialize connection to Gemini API
        
        Raises:
            APIError: If initialization fails
        """
        try:
            # Get current API key
            current_key = self.api_key_manager.get_current_key()
            genai.configure(api_key=current_key)
            
            # Auto-detect best model
            self.model_name = self._get_best_model()
            self.model = genai.GenerativeModel(self.model_name)
            
            logger.info("Connected to Google AI Studio")
            logger.info(f"Using model: {self.model_name}")
            logger.info(
                f"Using API key index: {self.api_key_manager.get_key_index()}/"
                f"{self.api_key_manager.get_total_keys()}"
            )
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            raise APIError(f"Cannot connect to Google AI Studio: {e}")
    
    def _get_best_model(self) -> str:
        """
        Auto-detect the best available Gemini model
        
        Tries preferred models in order and falls back to first available
        model that supports generateContent.
        
        Returns:
            Model name string
            
        Raises:
            APIError: If no compatible models found
        """
        preferred_models = [
            'gemini-2.0-flash-exp',
            'gemini-exp-1206',
            'gemini-2.0-flash-thinking-exp-1219',
            'gemini-exp-1121',
            'gemini-1.5-pro',
            'gemini-1.5-flash',
            'gemini-pro'
        ]
        
        try:
            available_models = genai.list_models()
            available_names = [
                m.name.replace('models/', '') for m in available_models
            ]
            
            # Return first preferred model that's available
            for model in preferred_models:
                if model in available_names:
                    logger.debug(f"Selected model: {model}")
                    return model
            
            # Fallback to first available model with generateContent
            for model in available_models:
                if 'generateContent' in model.supported_generation_methods:
                    name = model.name.replace('models/', '')
                    logger.warning(f"Using fallback model: {name}")
                    return name
            
            raise APIError("No compatible Gemini models found")
            
        except Exception as e:
            logger.warning(f"Could not auto-detect model: {e}. Using fallback.")
            return 'gemini-1.5-flash'
    
    def get_model(self) -> genai.GenerativeModel:
        """
        Get the configured Gemini model
        
        Returns:
            GenerativeModel instance
            
        Raises:
            APIError: If model not initialized
        """
        if self.model is None:
            raise APIError("Gemini model not initialized")
        
        return self.model
    
    def get_model_name(self) -> str:
        """
        Get the current model name
        
        Returns:
            Model name string
        """
        return self.model_name or "unknown"
    
    def reinitialize(self) -> None:
        """
        Reinitialize client (useful after key rotation)
        
        Raises:
            APIError: If reinitialization fails
        """
        logger.info("Reinitializing Gemini client")
        self._initialize()
