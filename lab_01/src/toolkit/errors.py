class ToolkitError(Exception):
    """Base exception for all toolkit errors."""


class CalculatorError(ToolkitError):
    """Exception raised for calculator errors."""


class ConverterError(ToolkitError):
    """Exception raised for converter errors."""


    