# system-info-cli

A lightweight CLI tool to display real-time system information — CPU, memory, disk, and network — built with Python and `psutil`.

## Setup

```bash
# Clone the repo and navigate into it
cd system-info-cli

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Show all system info (default)
python3 main.py

# Show specific sections
python3 main.py --cpu
python3 main.py --memory
python3 main.py --disk
python3 main.py --network

# Show all explicitly
python3 main.py --all

# Help
python3 main.py --help
```

## Example Output

```
────────────────────────────────────────
  CPU
────────────────────────────────────────
  Brand         : Apple M4
  Physical Cores: 10
  Logical Cores : 10
  Frequency     : 4 GHz
  Avg Usage     : 5.2%
  ⏱  collected in 1.52s

────────────────────────────────────────
  MEMORY
────────────────────────────────────────
  Total         : 16.0 GB
  Used          : 7.33 GB
  Available     : 5.8 GB
  Usage         : 63.7%
  ⏱  collected in 0.00s
```

## Project Structure

```
system-info-cli/
├── sysinfo/
│   ├── __init__.py
│   ├── cpu.py        # CPU brand, cores, frequency, usage (generator sampling)
│   ├── memory.py     # RAM total, used, available
│   ├── disk.py       # Disk partitions, usage per mount
│   └── network.py    # Network interfaces, bytes sent/received
├── main.py           # CLI entry point (argparse + @timed decorator)
└── requirements.txt
```

## Tech

- Python 3.14
- [`psutil`](https://github.com/giampaolo/psutil) — cross-platform system info
- `argparse` — CLI argument parsing (stdlib)
- `dataclasses` — typed data models (stdlib)
