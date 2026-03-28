import psutil
from dataclasses import dataclass


@dataclass
class DiskPartitionInfo:
    device: str
    mountpoint: str
    fstype: str
    total_gb: float
    used_gb: float
    free_gb: float
    usage_percent: float


def _bytes_to_gb(bytes_val: int) -> float:
    return round(bytes_val / (1024 ** 3), 2)


def get_disk_info() -> list[DiskPartitionInfo]:
    partitions = psutil.disk_partitions()

    result = []
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            result.append(DiskPartitionInfo(
                device=partition.device,
                mountpoint=partition.mountpoint,
                fstype=partition.fstype,
                total_gb=_bytes_to_gb(usage.total),
                used_gb=_bytes_to_gb(usage.used),
                free_gb=_bytes_to_gb(usage.free),
                usage_percent=usage.percent,
            ))
        except PermissionError:
            continue

    return result