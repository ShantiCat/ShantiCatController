"""Deduplication and sequence tracking for collar measurements."""

from dataclasses import dataclass

from shanti_cat_controller.protocol import CollarMeasurement


@dataclass(frozen=True, slots=True)
class SequenceResult:
    """Result of processing a measurement sequence number."""

    duplicate: bool
    missed_packets: int


class MeasurementSequenceTracker:
    """Track duplicate and missing collar measurements."""

    MAX_SEQUENCE = 0xFFFF
    SEQUENCE_RANGE = MAX_SEQUENCE + 1

    def __init__(self) -> None:
        """Initialize the sequence tracker."""

        self._last_sequence_by_device: dict[str, int] = {}

    def process(
        self,
        measurement: CollarMeasurement,
    ) -> SequenceResult:
        """Process a measurement sequence number."""

        current_sequence = measurement.sequence_number
        last_sequence = self._last_sequence_by_device.get(
            measurement.address,
        )

        if last_sequence is None:
            self._last_sequence_by_device[measurement.address] = (
                current_sequence
            )

            return SequenceResult(
                duplicate=False,
                missed_packets=0,
            )

        if current_sequence == last_sequence:
            return SequenceResult(
                duplicate=True,
                missed_packets=0,
            )

        difference = (
            current_sequence - last_sequence
        ) % self.SEQUENCE_RANGE

        missed_packets = max(0, difference - 1)

        self._last_sequence_by_device[measurement.address] = (
            current_sequence
        )

        return SequenceResult(
            duplicate=False,
            missed_packets=missed_packets,
        )