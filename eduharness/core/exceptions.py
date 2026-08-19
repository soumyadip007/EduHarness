class EduHarnessError(Exception):
    """Base exception for EduHarness."""


class ConfigError(EduHarnessError):
    """Raised when loading or validating config fails."""


class ContractError(EduHarnessError):
    """Raised when contract resolution fails."""
