"""Data models for received BLE advertisements."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True, slots=True)
class CollarAdvertisement:
    """Raw BLE advertisement received from a ShantiCat collar."""

    received_at: datetime
    address: str
    name: str
    rssi: int
    manufacturer_data: dict[int, bytes] = field(default_factory=dict)
    service_data: dict[str, bytes] = field(default_factory=dict)
    service_uuids: tuple[str, ...] = ()