from spidev import SpiDev
from time import sleep
from bit_utils import extract_bit,print_feature_table

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


