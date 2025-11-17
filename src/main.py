import spidev
from spi_helper import get_features, check_chip

# Create SPI object
spi = spidev.SpiDev()
spi.open(0, 0)  # bus 0, device 0
spi.max_speed_hz = 50000

print("Checking Chip")
check_chip(spi)

# Send and receive data
print("Get features")
get_features(spi)



spi.close()
