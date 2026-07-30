"""Main ShantiCat controller."""

import asyncio
import logging

from .ble import CollarAdvertisement, CollarAdvertisementCollector
from .protocol import (
    CollarAdvertisementDecoder,
    CollarMeasurement,
    ProtocolDecodeError,
)
from .processing import MeasurementSequenceTracker


logger = logging.getLogger(__name__)


class Controller:
    """Coordinate ShantiCat Controller components."""

    def __init__(self) -> None:
        """Initialize the controller."""

        self._collector = CollarAdvertisementCollector()
        self._decoder = CollarAdvertisementDecoder(
            manufacturer_id=0xFFFF,
        )
        self._sequence_tracker = MeasurementSequenceTracker()

    def run(self) -> None:
        """Run the controller."""

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        )

        try:
            asyncio.run(self._run())
        except KeyboardInterrupt:
            print("\nShantiCat Controller stopped.")

    async def _run(self) -> None:
        """Start controller components."""

        await self._collector.start()

        print("Listening for ShantiCatCollar advertisements...")
        print("Press Ctrl+C to stop.\n")

        try:
            async for advertisement in self._collector.advertisements():
                self._handle_advertisement(advertisement)
        finally:
            await self._collector.stop()

    def _handle_advertisement(
        self,
        advertisement: CollarAdvertisement,
    ) -> None:
        """Decode and process a collar advertisement."""

        try:
            measurement = self._decoder.decode(advertisement)
        except ProtocolDecodeError as error:
            logger.warning(
                "Invalid packet from %s: %s",
                advertisement.address,
                error,
            )
            return

        if measurement is None:
            logger.debug(
                "No ShantiCat manufacturer data in packet from %s",
                advertisement.address,
            )
            return

        sequence_result = self._sequence_tracker.process(measurement)

        if sequence_result.duplicate:
            logger.debug(
                "Duplicate packet from %s with sequence %d",
                measurement.address,
                measurement.sequence_number,
            )
            return

        if sequence_result.missed_packets:
            logger.warning(
                "Missed %d packet(s) from %s before sequence %d",
                sequence_result.missed_packets,
                measurement.address,
                measurement.sequence_number,
            )

        self._print_measurement(measurement)

    @staticmethod
    def _print_measurement(
        measurement: CollarMeasurement,
    ) -> None:
        """Print a decoded collar measurement."""

        print(f"Time:     {measurement.received_at.isoformat()}")
        print(f"Address:  {measurement.address}")
        print(f"RSSI:     {measurement.rssi} dBm")
        print(f"Version:  {measurement.protocol_version}")
        print(f"Samples:  {measurement.sample_count}")
        print(f"Sequence: {measurement.sequence_number}")
        print(
            "Accel:    "
            f"X={measurement.acceleration_x}, "
            f"Y={measurement.acceleration_y}, "
            f"Z={measurement.acceleration_z}"
        )
        print("-" * 60)