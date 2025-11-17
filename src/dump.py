from spidev import SpiDev
from typing import IO

class SPIDump:
    def __init__(self, spi: SpiDev, file: IO):
        """
        Initialize the SPI dump with an existing SpiDev object and a file-like object.
        """
        self.__spi = spi        # use the passed SpiDev instance
        self.__file = file      # store the file object

    def dump(self):
        result=self.__spi.xfer2([0x13,0x00,0x00,0x00])
        result=self.__spi.xfer2([0x31,0x00,0x00,0x00])
