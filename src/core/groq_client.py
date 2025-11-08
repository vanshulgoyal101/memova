"""
Groq AI client wrapper with Gemini-compatible interface
Provides seamless integration with existing codebase
"""

from typing import Optional
from groq import Groq

from src.utils.logger import setup_logger
from src.utils.exceptions import APIError

logger = setup_logger(__name__)


class GroqResponse:
    """
    Wrapper to match Gemini GenerateContentResponse format
    
    Provides .text property for compatibility with existing code
    """
    
    def __init__(self, content: str):
        """
        Initialize response wrapper
        
        Args:
            content: Generated text content
        """
        self.text = content


class GroqModel:
    """
    Wrapper to match Gemini GenerativeModel interface
    
    Provides generate_content() method for compatibility
    """
    
    def __init__(self, client: Groq, model_name: str):
        """
        Initialize model wrapper
        
        Args:
            client: Groq client instance
            model_name: Model identifier (e.g., "llama-3.3-70b-versatile")
        """
        self.client = client
        self.model_name = model_name
    
    def generate_content(self, prompt: str, system_message: str = None) -> GroqResponse:
        """
        Generate content matching Gemini interface with optional system message
        
        When system_message is provided, it's sent as a separate system role message,
        which allows Groq's automatic prefix caching to cache the system prompt
        across multiple requests, significantly reducing token usage.
        
        Args:
            prompt: Input prompt for generation (user message)
            system_message: Optional system instructions (cached by Groq)
            
        Returns:
            GroqResponse with .text property
            
        Raises:
            APIError: If generation fails
        """
        try:
            logger.debug(f"Groq generating with model: {self.model_name}")
            
            # Build messages array with system message first (for caching)
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.1,  # Low temperature for consistent SQL generation
                max_tokens=500,   # Sufficient for SQL queries
                top_p=1,
            )
            
            content = response.choices[0].message.content
            
            if not content:
                raise APIError("Groq returned empty response")
            
            # Log token usage for monitoring
            if hasattr(response, 'usage') and response.usage:
                usage = response.usage
                total = usage.total_tokens
                prompt = usage.prompt_tokens
                completion = usage.completion_tokens
                
                logger.info(f"🔢 Groq tokens: {total} total ({prompt} prompt + {completion} completion)")
                
                # Check for cached tokens (only available for some models)
                if hasattr(usage, 'prompt_tokens_details') and usage.prompt_tokens_details:
                    cached = getattr(usage.prompt_tokens_details, 'cached_tokens', 0)
                    if cached > 0:
                        logger.info(f"✅ Cache hit: {cached} tokens cached! ({(cached/prompt*100):.1f}% of prompt)")
                    elif system_message:
                        logger.debug(f"ℹ️  No cache metrics (model may cache without exposing metrics)")
            
            # Note: Caching metrics (prompt_tokens_details.cached_tokens) are only
            # available for certain models (kimi-k2-instruct, gpt-oss-*) per Groq docs.
            # llama-3.3-70b-versatile DOES cache (confirmed by 88% speed improvement
            # on cached requests), but metrics are not exposed in API response yet.
            # Groq is rolling out caching support to more models over time.
            
            logger.debug(f"Groq generated {len(content)} characters")
            
            return GroqResponse(content)
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Groq API error: {error_msg}")
            
            # Provide helpful context for rate limit errors
            if "rate_limit" in error_msg.lower() or "429" in error_msg:
                if "org_" in error_msg:
                    logger.warning(
                        "⚠️  GROQ RATE LIMIT: All your API keys belong to the same organization. "
                        "Rate limits are per-organization, not per-key. "
                        "To increase capacity, create API keys from different Groq accounts (different emails)."
                    )
            
            # Re-raise with context
            raise APIError(f"Groq generation failed: {error_msg}")


class GroqClient:
    """
    Wrapper for Groq AI client with Gemini-compatible interface
    
    Provides seamless drop-in replacement for GeminiClient in existing code.
    
    Features:
    - Automatic model selection (llama-3.3-70b-versatile preferred)
    - Same interface as GeminiClient (get_model, get_model_name)
    - Compatible response format (.text property)
    
    Example:
        >>> client = GroqClient(api_key="gsk_...")
        >>> model = client.get_model()
        >>> response = model.generate_content("SELECT * FROM users")
        >>> print(response.text)
    """
    
    # Preferred models in order (best to fallback)
    PREFERRED_MODELS = [
        'llama-3.3-70b-versatile',     # Best for SQL (70B params, 128k context)
        'llama-3.1-70b-versatile',     # Alternative 70B model
        'mixtral-8x7b-32768',          # Mixture of Experts (56B active, 32k context)
        'llama-3.1-8b-instant',        # Fastest (8B params, good for simple queries)
    ]
    
    def __init__(self, api_key: str):
        """
        Initialize Groq client
        
        Args:
            api_key: Groq API key (starts with "gsk_")
            
        Raises:
            APIError: If API key is invalid or client initialization fails
        """
        if not api_key:
            raise APIError("Groq API key is required")
        
        if api_key == "your-groq-api-key-here":
            raise APIError(
                "Please set a valid Groq API key in .env\n"
                "Get free key: https://console.groq.com/"
            )
        
        try:
            self.api_key = api_key
            # Initialize Groq client with only the API key
            # Note: The Groq SDK uses httpx internally but doesn't accept proxy config directly
            self.client = Groq(api_key=api_key)
            self.model_name = self._get_best_model()
            self.model = GroqModel(self.client, self.model_name)
            
            logger.info(f"GroqClient initialized")
            logger.info(f"Using model: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            raise APIError(f"Groq initialization failed: {e}")
    
    def _get_best_model(self) -> str:
        """
        Select best available Groq model
        
        Tries preferred models in order. Falls back to first available
        if none match (useful for future model updates).
        
        Returns:
            Model name string
        """
        # For now, use first preferred model
        # In production, could query Groq API for available models
        # and select best match
        selected_model = self.PREFERRED_MODELS[0]
        
        logger.debug(f"Selected Groq model: {selected_model}")
        
        return selected_model
    
    def get_model(self) -> GroqModel:
        """
        Get the configured Groq model (Gemini-compatible)
        
        Returns:
            GroqModel instance with generate_content() method
            
        Raises:
            APIError: If model not initialized
        """
        if self.model is None:
            raise APIError("Groq model not initialized")
        
        return self.model
    
    def get_model_name(self) -> str:
        """
        Get the current model name for logging
        
        Returns:
            Model name string (e.g., "llama-3.3-70b-versatile")
        """
        return self.model_name or "unknown"
    
    def reinitialize(self) -> None:
        """
        Reinitialize client (for compatibility with GeminiClient)
        
        Note: Groq doesn't need reinitialization like Gemini's key rotation,
        but we provide this method for interface compatibility.
        """
        logger.debug("GroqClient reinitialize called (no-op)")
        # No action needed - Groq uses single key
