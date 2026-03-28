import psutil
from dataclasses import dataclass

@dataclass
class MemoryInfo:
    total_gb: float
    available_gb: float
    used_gb: float
    usage_percent: float

def _bytes_to_gb(bytes_val: int) -> float:
    return round(bytes_val / (1024 ** 3), 2)

def get_memory_info() -> MemoryInfo:
    mem = psutil.virtual_memory()

    return MemoryInfo(
        total_gb=_bytes_to_gb(mem.total),
        available_gb=_bytes_to_gb(mem.available),
        used_gb=_bytes_to_gb(mem.used),
        usage_percent=mem.percent,
    )