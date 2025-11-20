from spidev import SpiDev
from typing import IO
from time import sleep
import os

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
    def __init__(self, spi: SpiDev,
                 file: IO,
                 total_blocks: int = 1024,
                 pages_per_block: int = 64,
                 page_size: int = 2112):
        """
        Initialize the SPI dump with an existing SpiDev object and a file-like object.
        :spi: The Interface used from flash rom
        :file: The file handler to dump flash
        :total_blocks: blocks flash memory has
        :pages_per_block: total pages flash memory has
        :page_size: bumber of bytes each page has
        """
        self.__spi = spi
        self.__file = file

        self.__total_blocks=total_blocks
        self.__pages_per_block=pages_per_block
        self.__page_size=page_size


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

        for block in range(self.__total_blocks):
            for page in range(self.__pages_per_block):
                print(f"dumping block {block} page {page}")
                if (page == self.__pages_per_block-1):
                    (result, status) = self.__send_command(0x3F, [0x00, 0x00, 0x00])
                else:
                    (result, status) = self.__send_command(0x31, page_addr)

                cmd = [0x03, 0x00, 0x00, 0]
                # By padding data we allow it to read data
                pad = [0x00] * self.__page_size
                resp = self.__spi.xfer2(cmd+pad)

                poll_operation_complete(self.__spi)

                self.__file.write(bytearray(resp))
                self.__file.flush()
                os.fsync(self.__file.fileno())