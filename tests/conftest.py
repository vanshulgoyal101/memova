"""
Pytest configuration and shared fixtures
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session", autouse=True)
def reset_api_keys_session():
    """
    Reset failed API keys at the start of test session
    
    This prevents cascading failures when keys are marked as failed
    during rapid test execution. The singleton key managers persist
    state across tests, so we reset at session start.
    """
    try:
        from src.core.api_key_manager import APIKeyManager
        from src.core.groq_key_manager import GroqKeyManager
        
        # Reset Gemini keys
        gemini_manager = APIKeyManager()
        gemini_manager.reset_failed_keys()
        
        # Reset Groq keys
        groq_manager = GroqKeyManager()
        groq_manager.reset_failed_keys()
        
        print("\n✓ Reset API key managers for test session")
    except Exception as e:
        print(f"\n⚠ Could not reset API keys: {e}")
    
    yield  # Run tests
    
    # Optional: Reset again after session (for local dev)
    try:
        gemini_manager.reset_failed_keys()
        groq_manager.reset_failed_keys()
        print("\n✓ Reset API key managers after test session")
    except:
        pass


@pytest.fixture(scope="session")
def project_root_path():
    """Return project root path"""
    return Path(__file__).parent.parent


@pytest.fixture
def reset_api_keys():
    """
    Reset failed API keys before a test
    
    Use this fixture in tests that make many API calls or
    when you need fresh key state. Example:
    
        def test_many_queries(reset_api_keys):
            # Keys are reset, all available
            ...
    """
    try:
        from src.core.api_key_manager import APIKeyManager
        from src.core.groq_key_manager import GroqKeyManager
        
        APIKeyManager().reset_failed_keys()
        GroqKeyManager().reset_failed_keys()
    except Exception:
        pass  # Fail silently if managers not initialized
    
    yield  # Run test


@pytest.fixture(scope="session")
def data_dir(project_root_path):
    """Return data directory path"""
    return project_root_path / "data"


@pytest.fixture(scope="session")
def electronics_db_path(data_dir):
    """Return electronics database path"""
    return data_dir / "database" / "electronics_company.db"


@pytest.fixture(scope="session")
def airline_db_path(data_dir):
    """Return airline database path"""
    return data_dir / "database" / "airline_company.db"


@pytest.fixture(scope="session")
def databases_exist(electronics_db_path, airline_db_path):
    """Check if both databases exist"""
    return electronics_db_path.exists() and airline_db_path.exists()


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "requires_db: marks tests that require databases to be generated"
    )
    config.addinivalue_line(
        "markers", "requires_api: marks tests that require API key"
    )
