"""
Custom exceptions for the application
"""


class AppException(Exception):
    """Base exception for application"""
    pass


class ConfigurationError(AppException):
    """Configuration related errors"""
    pass


class DatabaseError(AppException):
    """Database related errors"""
    pass


class DataGenerationError(AppException):
    """Data generation errors"""
    pass


class QueryError(AppException):
    """Query execution errors"""
    pass


class ValidationError(AppException):
    """Data validation errors"""
    pass


class APIError(AppException):
    """API related errors"""
    pass
