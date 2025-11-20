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
