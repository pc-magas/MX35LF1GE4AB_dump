from spidev import SpiDev
from typing import IO
from time import sleep

def poll_operation_complete(spi:SpiDev)-> int:
    """
    Poll the flash until the OIP (Operation In Progress) bit clears in feature address 0xC0.
    
    :param spi: Initialized SpiDev instance
    :return: Final status byte of register 0xC0
    """

    status=None
    while True:
        resp = spi.xfer2([0x0F, 0xC0, 0x00])
        status = resp[2]
        oip = status & 0x1
        if oip == 0:
            break
        sleep(0.001)
    
    return status

class SPIDump:
    def __init__(self, spi: SpiDev, file: IO):
        """
        Initialize the SPI dump with an existing SpiDev object and a file-like object.
        """
        self.__spi = spi        # use the passed SpiDev instance
        self.__file = file      # store the file object

    def __reset(self):
        self.__spi.xfer2([0xFF])
        poll_operation_complete(self.__spi)

    def __send_command(self, command: int, address: list)->(list,int):
        result = self.__spi.xfer2([command] + address)
        status = poll_operation_complete(self.__spi)
        return result, status

    def dump(self):
        self.__reset()
        page_addr = [0x00, 0x00, 0x00]

        # PAGE READ (0x13)
        (result,status)=self.__send_command(0x13, page_addr)

        # READ (0x31)
        (result,status) = self.__send_command(0x31, page_addr)
