import argparse
import spidev
from spi_helper import get_features, check_chip
from dump import SPIDump
from file import open_file

# Create SPI object
spi = spidev.SpiDev()
spi.open(0, 0)  # bus 0, device 0
spi.max_speed_hz = 50000

print("Checking Chip")
check_chip(spi)

# Send and receive data
print("Get features")
get_features(spi)

parser = argparse.ArgumentParser(description="SPI flash dump to file")
parser.add_argument("filename", help="Output file to save the flash dump")
args = parser.parse_args()
filename = args.filename

with open_file(filename) as f:
    print("################################")
    print(f"DUMPING DATA upon {filename}")
    dump = SPIDump(spi, f)
    dump.dump()

print("Terminate connections")
spi.close()
print("Exit")
