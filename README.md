# ALDL Logger

A Python tool for logging 160 baud data from GM's [Assembly Line Diagnostic Link](https://en.wikipedia.org/wiki/ALDL) interface. This tool is designed to work with an FTDI FT232R-based ALDL cable (like those from [aldlcable.com](http://aldlcable.com/)).

I bought a [Howell TBI kit](https://howellefi.com/product/tbi-kit-1981-86-cj-4-2l-emissions-legal/) for my 88 Jeep YJ which included a GM 1227747 ECU. This pre-dates OBD2 and includes an ALDL 12-pin interface that transmits serial-ish data at 160 baud. 

Both the 160 baud rate and the signaling protocol is somewhat non-standard, so the best way to read this seems to be to run the port at 10x speed - 1600 baud - and then sample the center bit to read each bit of the ALDL stream. Thanks to Tech Edge's excellent write up of this for the explainer (https://www.techedge.com.au/vehicle/aldl160/160serial.htm).

Most information (and programs to read or decode it) seems to have disappeared from the Internet at this point, so hopefully folks find this useful. 

See my [aldl-webusb](https://github.com/alexlinde/aldl-webusb) project if you want a way to visualize this. 

## Features

- Reads ALDL data at 160 baud using an FT232R-based serial cable
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
