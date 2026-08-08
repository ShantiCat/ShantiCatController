"""Decoder for ShantiCat BLE advertisement payloads."""

import struct

from shanti_cat_controller.ble import CollarAdvertisement

from .exceptions import InvalidPayloadLengthError
from .measurement import CollarMeasurement


class CollarAdvertisementDecoder:
    """Decode ShantiCat manufacturer-specific BLE data."""

    # Little-endian:
    # B - protocol version
    # B - sample count or packet type
    # H - sequence number
    # h - acceleration X
    # h - acceleration Y
    # h - acceleration Z
    # h - gyroscope X
    # h - gyroscope Y
    # h - gyroscope Z
    # H  battery_voltage_mv
    PAYLOAD_STRUCT = struct.Struct("<BBHhhhhhhH")

    def __init__(self, manufacturer_id: int = 0xFFFF) -> None:
        """Initialize the decoder."""

        self._manufacturer_id = manufacturer_id

    def decode(
        self,
        advertisement: CollarAdvertisement,
    ) -> CollarMeasurement | None:
        """Decode one ShantiCat advertisement."""

        payload = advertisement.manufacturer_data.get(
            self._manufacturer_id,
        )

        if payload is None:
            return None

        if len(payload) != self.PAYLOAD_STRUCT.size:
            raise InvalidPayloadLengthError(
                f"Expected {self.PAYLOAD_STRUCT.size} payload bytes, "
                f"received {len(payload)}: {payload.hex(' ')}"
            )

        (
            protocol_version,
            sample_count,
            sequence_number,
            acceleration_x,
            acceleration_y,
            acceleration_z,
            gyroscope_x,
            gyroscope_y,
            gyroscope_z,
            battery_voltage_mv,
        ) = self.PAYLOAD_STRUCT.unpack(payload)

        return CollarMeasurement(
            received_at=advertisement.received_at,
            address=advertisement.address,
            rssi=advertisement.rssi,
            protocol_version=protocol_version,
            sample_count=sample_count,
            sequence_number=sequence_number,
            acceleration_x=acceleration_x,
            acceleration_y=acceleration_y,
            acceleration_z=acceleration_z,
            gyroscope_x=gyroscope_x,
            gyroscope_y=gyroscope_y,
            gyroscope_z=gyroscope_z,
            battery_voltage_mv=battery_voltage_mv,
        )