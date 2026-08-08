"""Decoded ShantiCat collar measurements."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class CollarMeasurement:
    """IMU measurement decoded from a collar advertisement."""

    received_at: datetime
    address: str
    rssi: int

    protocol_version: int
    sample_count: int
    sequence_number: int

    acceleration_x: int
    acceleration_y: int
    acceleration_z: int

    gyroscope_x: int
    gyroscope_y: int
    gyroscope_z: int

    battery_voltage_mv: int