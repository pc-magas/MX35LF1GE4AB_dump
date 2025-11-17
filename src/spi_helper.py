from spidev import SpiDev
from time import sleep

def extract_bit(value: int, bit_index: int) -> bool:
    """
    Extract the i-th bit of a byte and return True if it is 1, False if 0.

    :param value: Integer value (0-255)
    :param bit_index: Bit position (0 = LSB, 7 = MSB)
    :return: True if bit is 1, False if 0
    """
    return ((value >> bit_index) & 1) == 1

def print_feature_table(feature_value, bit_definitions):
    """
    Prints a table showing each bit's name and its value (enabled/disabled).

    :param feature_value: int, the feature register value (0-255)
    :param bit_definitions: dict, mapping bit positions to names {7: 'Secure OTP Protect', 6: 'Secure OTP Enable', ...}
                            Bits not defined will be labeled 'Reserved'
    """
    print(f"Feature register value: 0x{feature_value:02X}  (0b{feature_value:08b})\n")
    print(f"{'Bit':>3} | {'Name':<25} | {'Enabled?'}")
    print("-"*40)

    for bit in range(7, -1, -1):
        name = bit_definitions.get(bit, 'Reserved')
        enabled = extract_bit(feature_value, bit)
        status = 'Yes' if enabled else 'No'
        print(f"{bit:>3} | {name:<25} | {status}")

def check_chip(spi:SpiDev):
    """
    Checks chip manuifacturer and type
    It exists if wrong type
    """
    resp = spi.xfer2([0x9F, 0x00, 0x00, 0x00])
    if(resp[2] == 0xC2):
        print("Macronix MX35LF1GE4AB found")
        if(resp[3] == 0x12):
            print("Device type is SERIAL NAND flash chip")
        else:
            print("Uknown type")
            exit(1)
    else:
        print("Device not found")
        exit(1)


def get_features(spi:SpiDev):
    """
    Iterate over feature register addresses, read via SPI, and print a table.
    """

    addresses={
        0xB0:{
            7: "Secure OTP Protect",
            6: "Secure OTP Enable",
            5: "Reserved",
            4: "ECC Enabled",
            3: "Reserved",
            2: "Reserved",
            1: "Reserved",
            0: "QE"
        },
        0xC0: {
            7: "Reserved",
            6: "CRBSY",
            5: "ECC_S1",
            4: "ECC_S0",
            3: "P_Fail",
            2: "E_Fail",
            1: "WEL",
            0: "OIP"
        },
        0xA0:{
            7: "BPRWD",
            6: "Reserved",
            5: "BP2",
            4: "BP1",
            3: "BP0",
            2: "Invert",
            1: "Complementary",
            0: "SP"
        }
    }

    
    for reg_addr, bit_defs in addresses.items():
        # SPI GET FEATURE command: 0x0F, reg_addr, then a dummy byte to clock out the response
        resp = spi.xfer2([0x0F, reg_addr, 0x00])
        feature_value = resp[2]  # actual register value
        print(f"\n--- Feature Register 0x{reg_addr:02X} ---")
        print_feature_table(feature_value, bit_defs)



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
