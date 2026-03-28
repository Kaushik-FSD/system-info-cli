from dataclasses import dataclass
import psutil
from typing import Generator

@dataclass
class CPUInfo:
    brand: str
    physical_cores: int
    logical_cores: int
    max_freq_mhz: float
    current_freq_mhz: float
    average_usage_percent: float

# Generator[YieldType, SendType, ReturnType]
def _sample_cpu_usage(samples: int) -> Generator[float, None, None]:
    for _ in range(samples):
        yield psutil.cpu_percent(interval=0.5)

def platform_cpu_brand() -> str:
    try:
        import subprocess
        result = subprocess.run(
            ["sysctl", "-n", "machdep.cpu.brand_string"],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception:
        return "Unknown"
    
def get_cpu_info() -> CPUInfo:
    freq = psutil.cpu_freq()
    usage_sample = list(_sample_cpu_usage(3))
    average_usage = sum(usage_sample) / len(usage_sample)

    return CPUInfo(
        brand=platform_cpu_brand(),
        physical_cores=psutil.cpu_count(logical=False),
        logical_cores=psutil.cpu_count(logical=True),
        max_freq_mhz=round(freq.max, 2),
        current_freq_mhz=round(freq.current, 2),
        average_usage_percent=round(average_usage, 2),
    )