import time
from typing import List, Optional
import pyftdi.serialext
from datetime import datetime
import json

class ALDLReader:
    def __init__(self, port: str):
        self.serial = pyftdi.serialext.serial_for_url(
            port, 
            baudrate=1600,
            timeout=1)
        
    def read_aldl_bit(self) -> Optional[bool]:
        """Read a single ALDL bit from the serial port by reading 1 byte and sampling the 4th bit"""
        byte = self.serial.read(1)
        if not byte:
            return None
        return not bool(ord(byte) & 0x08)
    
    def read_aldl_byte(self) -> Optional[int]:
        """Read a complete ALDL byte (8 data bits, MSB first)"""
        byte_value = 0
        for _ in range(8):  
            bit = self.read_aldl_bit()
            if bit is None:
                return None
            byte_value = (byte_value << 1) | (1 if bit else 0)        
        return byte_value
    
    def wait_for_sync(self) -> bool:
        """Wait for the ALDL sync pattern (9 bits of value 1)"""
        sync_bits = 0
        while sync_bits < 9:
            bit = self.read_aldl_bit()
            if bit is None:
                return False
            if bit:
                sync_bits += 1
            else:
                sync_bits = 0
        return True
        
    def read_aldl_frame(self) -> Optional[List[int]]:
        """Read a complete ALDL frame (20 data bytes after sync)"""
        # Wait for sync pattern (9 bits of 1)
        if not self.wait_for_sync():
            return None
        
        # Read 20 data bytes
        frame = []
        for _ in range(20):
            # Check for premature sync start
            bit = self.read_aldl_bit()
            if bit:
                print("Warning: Sync pattern detected during frame - discarding incomplete frame")
                return None
            
            byte = self.read_aldl_byte()
            if byte is None:
                return None
            frame.append(byte)
        
        return frame
    
    def close(self):
        """Close the serial connection"""
        self.serial.close()

def main():
    # Create timestamped filename, log as json
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"aldl_log_{timestamp}.json"
    
    # Looking for an FT232R, i.e. 
    # http://aldlcable.com/
    reader = ALDLReader('ftdi://ftdi:232r/1')
    try:
        print("Starting ALDL data logging...")
        print(f"Logging to file: {filename}")
        print("Press Ctrl+C to stop")
        
        with open(filename, 'w') as log_file:
            log_file.write('[\n')
            first_frame = True
            while True:
                frame = reader.read_aldl_frame()
                if frame:
                    timestamp = datetime.now().isoformat()
                    frame_data = {
                        "timestamp": timestamp,
                        "frame": frame
                    }
                    json_line = json.dumps(frame_data)
                    if not first_frame:
                        log_file.write(',\n')
                    log_file.write(json_line)
                    hex_frame = ' '.join(f'{b:02X}' for b in frame)
                    print(hex_frame)
                    log_file.flush()
                    first_frame = False
                time.sleep(0.001) 
            
    except KeyboardInterrupt:
        print("\nStopping ALDL logger...")
    finally:
        with open(filename, 'a') as log_file:
            log_file.write('\n]')
        reader.close()

if __name__ == "__main__":
    main() 