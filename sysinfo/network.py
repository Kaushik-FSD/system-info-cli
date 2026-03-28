import psutil
from dataclasses import dataclass


@dataclass
class NetworkInterfaceInfo:
    interface: str
    bytes_sent_mb: float
    bytes_recv_mb: float
    packets_sent: int
    packets_recv: int


def _bytes_to_mb(bytes_val: int) -> float:
    return round(bytes_val / (1024 ** 2), 2)


def get_network_info() -> list[NetworkInterfaceInfo]:
    io_counters = psutil.net_io_counters(pernic=True)

    return [
        NetworkInterfaceInfo(
            interface=interface,
            bytes_sent_mb=_bytes_to_mb(stats.bytes_sent),
            bytes_recv_mb=_bytes_to_mb(stats.bytes_recv),
            packets_sent=stats.packets_sent,
            packets_recv=stats.packets_recv,
        )
        for interface, stats in io_counters.items()
        if stats.bytes_sent > 0 or stats.bytes_recv > 0
    ]