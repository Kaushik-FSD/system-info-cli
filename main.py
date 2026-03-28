import argparse
import functools
import time

from sysinfo.cpu import get_cpu_info
from sysinfo.memory import get_memory_info
from sysinfo.disk import get_disk_info
from sysinfo.network import get_network_info


# ── Decorator ────────────────────────────────────────────────
def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  ⏱  collected in {elapsed:.2f}s\n")
        return result
    return wrapper


# ── Display helpers ───────────────────────────────────────────
def print_section(title: str) -> None:
    print(f"\n{'─' * 40}")
    print(f"  {title}")
    print(f"{'─' * 40}")


@timed
def show_cpu() -> None:
    print_section("CPU")
    info = get_cpu_info()
    print(f"  Brand         : {info.brand}")
    print(f"  Physical Cores: {info.physical_cores}")
    print(f"  Logical Cores : {info.logical_cores}")
    print(f"  Frequency     : {info.current_freq_mhz} GHz")
    print(f"  Avg Usage     : {info.average_usage_percent}%")


@timed
def show_memory() -> None:
    print_section("MEMORY")
    info = get_memory_info()
    print(f"  Total         : {info.total_gb} GB")
    print(f"  Used          : {info.used_gb} GB")
    print(f"  Available     : {info.available_gb} GB")
    print(f"  Usage         : {info.usage_percent}%")


@timed
def show_disk() -> None:
    print_section("DISK")
    partitions = get_disk_info()
    # filter to only meaningful partitions
    visible = [p for p in partitions if p.mountpoint in ("/", "/System/Volumes/Data")]
    for p in visible:
        print(f"  Mount         : {p.mountpoint}")
        print(f"  Total         : {p.total_gb} GB")
        print(f"  Used          : {p.used_gb} GB ({p.usage_percent}%)")
        print(f"  Free          : {p.free_gb} GB")
        print()


@timed
def show_network() -> None:
    print_section("NETWORK")
    interfaces = get_network_info()
    # filter to main wifi and loopback only
    visible = [i for i in interfaces if i.interface in ("en0", "lo0")]
    for i in visible:
        print(f"  Interface     : {i.interface}")
        print(f"  Sent          : {i.bytes_sent_mb} MB")
        print(f"  Received      : {i.bytes_recv_mb} MB")
        print(f"  Packets Sent  : {i.packets_sent}")
        print(f"  Packets Recv  : {i.packets_recv}")
        print()


# ── CLI entry point ───────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        prog="sysinfo",
        description="System information CLI tool"
    )
    parser.add_argument("--cpu",     action="store_true", help="Show CPU info")
    parser.add_argument("--memory",  action="store_true", help="Show memory info")
    parser.add_argument("--disk",    action="store_true", help="Show disk info")
    parser.add_argument("--network", action="store_true", help="Show network info")
    parser.add_argument("--all",     action="store_true", help="Show all info")

    args = parser.parse_args()

    ###
    show_all = args.all or not any([args.cpu, args.memory, args.disk, args.network])

    # Break it into parts:
    # **`any([False, False, False, False])`** → `False` — because none of them are truthy.
    # **`not False`** → `True`
    # **`args.all or True`** → `True`
    # So `show_all = True`.
    # Then every condition like `if show_all or args.cpu` becomes `if True or False` → runs.
    # ---
    # Now when you run `python3 main.py --cpu`:
    # args.cpu = True   ← only this is True

    # if no flags passed, default to --all
    show_all = args.all or not any([args.cpu, args.memory, args.disk, args.network])

    if show_all or args.cpu:
        show_cpu()
    if show_all or args.memory:
        show_memory()
    if show_all or args.disk:
        show_disk()
    if show_all or args.network:
        show_network()


if __name__ == "__main__":
    main()