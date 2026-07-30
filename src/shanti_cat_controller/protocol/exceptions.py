"""Exceptions raised while decoding ShantiCat protocol packets."""


class ProtocolDecodeError(ValueError):
    """Base exception for ShantiCat protocol decoding errors."""


class InvalidPayloadLengthError(ProtocolDecodeError):
    """Raised when a payload has an unexpected length."""


class InvalidMagicError(ProtocolDecodeError):
    """Raised when a payload does not contain the ShantiCat signature."""


class UnsupportedProtocolVersionError(ProtocolDecodeError):
    """Raised when a payload uses an unsupported protocol version."""


class InvalidBatteryLevelError(ProtocolDecodeError):
    """Raised when a payload contains an invalid battery level."""