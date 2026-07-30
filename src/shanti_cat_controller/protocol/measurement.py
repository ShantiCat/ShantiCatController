"""Decoded ShantiCat collar measurements."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class CollarMeasurement:
    """Acceleration measurement decoded from a collar advertisement."""

    received_at: datetime
    address: str
    rssi: int

    protocol_version: int
    sample_count: int
    sequence_number: int

    acceleration_x: int
    acceleration_y: int
    acceleration_z: int

    @property
    def acceleration_x_g(self) -> float:
        """Return acceleration along the X axis in g."""

        return self.acceleration_x_mg / 1000.0

    @property
    def acceleration_y_g(self) -> float:
        """Return acceleration along the Y axis in g."""

        return self.acceleration_y_mg / 1000.0

    @property
    def acceleration_z_g(self) -> float:
        """Return acceleration along the Z axis in g."""

        return self.acceleration_z_mg / 1000.0