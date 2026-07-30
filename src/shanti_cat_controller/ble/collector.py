"""BLE advertisement collector for ShantiCat collars."""

import asyncio
import logging
from collections.abc import AsyncIterator
from datetime import datetime, timezone

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from .advertisement import CollarAdvertisement


logger = logging.getLogger(__name__)


class CollarAdvertisementCollector:
    """Collect BLE advertisements transmitted by ShantiCat collars."""

    def __init__(
        self,
        device_name: str = "ShantiCatCollar",
        queue_size: int = 100,
    ) -> None:
        """Initialize the collector.

        Args:
            device_name:
                BLE local name used by ShantiCat collars.

            queue_size:
                Maximum number of advertisements waiting to be processed.
        """

        self._device_name = device_name
        self._queue: asyncio.Queue[CollarAdvertisement] = asyncio.Queue(
            maxsize=queue_size,
        )
        self._scanner: BleakScanner | None = None
        self._running = False

    @property
    def running(self) -> bool:
        """Return whether the BLE scanner is currently running."""

        return self._running

    async def start(self) -> None:
        """Start collecting BLE advertisements."""

        if self._running:
            return

        self._scanner = BleakScanner(
            detection_callback=self._handle_advertisement,
        )

        await self._scanner.start()
        self._running = True

        logger.info(
            "BLE advertisement collector started for device name %s",
            self._device_name,
        )

    async def stop(self) -> None:
        """Stop collecting BLE advertisements."""

        if not self._running:
            return

        if self._scanner is not None:
            await self._scanner.stop()

        self._scanner = None
        self._running = False

        logger.info("BLE advertisement collector stopped")

    async def get(self) -> CollarAdvertisement:
        """Wait for and return the next collar advertisement."""

        return await self._queue.get()

    async def advertisements(self) -> AsyncIterator[CollarAdvertisement]:
        """Yield collar advertisements as they are received."""

        while self._running:
            yield await self.get()

    def _handle_advertisement(
        self,
        device: BLEDevice,
        advertisement_data: AdvertisementData,
    ) -> None:
        """Handle an advertisement detected by Bleak."""

        device_name = advertisement_data.local_name or device.name

        if device_name != self._device_name:
            return

        advertisement = CollarAdvertisement(
            received_at=datetime.now(timezone.utc),
            address=device.address,
            name=device_name,
            rssi=advertisement_data.rssi,
            manufacturer_data=dict(advertisement_data.manufacturer_data),
            service_data=dict(advertisement_data.service_data),
            service_uuids=tuple(advertisement_data.service_uuids),
        )

        self._put_advertisement(advertisement)

    def _put_advertisement(
        self,
        advertisement: CollarAdvertisement,
    ) -> None:
        """Add an advertisement to the processing queue."""

        try:
            self._queue.put_nowait(advertisement)
        except asyncio.QueueFull:
            logger.warning(
                "Advertisement queue is full; dropping packet from %s",
                advertisement.address,
            )