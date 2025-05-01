# ALDL Logger

A Python tool for logging data from GM's Assembly Line Diagnostic Link (ALDL) interface. This tool is designed to work with an FTDI FT232R-based ALDL cable (like those from [aldlcable.com](http://aldlcable.com/)).

## Features

- Reads ALDL data at 160 baud
- Captures complete ALDL frames (20 bytes after sync) and logs in JSON format
- Compatible with FTDI FT232R-based ALDL cables

## Requirements

- Python 3.x
- pyftdi
- An FTDI FT232R-based ALDL cable

## Installation

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Connect your ALDL cable to your computer
2. Run the logger:
```bash
python aldl_logger.py
```

The program will:
- Create a timestamped JSON log file (e.g., `aldl_log_20240321_143045.json`)
- Display hex values of frames in real-time in the console
- Log complete frames with timestamps to the JSON file

Press Ctrl+C to stop logging.

## Output Format

The JSON log file contains an array of frame objects, each with:
- `timestamp`: ISO format timestamp
- `frame`: Array of 20 bytes from the ALDL interface

Example:
```json
[
  {
    "timestamp": "2024-03-21T14:30:45.123456",
    "frame": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
  }
]
```
