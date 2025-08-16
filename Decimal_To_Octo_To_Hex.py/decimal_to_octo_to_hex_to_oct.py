def decimal_to_hex(decimal: int) -> str:
    """
    Converts a decimal number to hexadecimal.
    
    Args:
        decimal (int): The decimal number to convert.
    
    Returns:
        str: The hexadecimal representation of the decimal number.
    """
    return hex(decimal)[2:]


def decimal_to_octal(decimal: int) -> str:
    """
    Converts a decimal number to octal.
    
    Args:
        decimal (int): The decimal number to convert.
    
    Returns:
        str: The octal representation of the decimal number.
    """
    return oct(decimal)[2:]


def hex_to_octal(hex_string: str) -> str:
    """
    Converts a hexadecimal number to octal.
    
    Args:
        hex_string (str): The hexadecimal number to convert.
    
    Returns:
        str: The octal representation of the hexadecimal number.
    """
    decimal = int(hex_string, 16)
    return oct(decimal)[2:]


def main():
    decimal = int(input("Enter a decimal number: "))
    
    hex_string = decimal_to_hex(decimal)
    octal_string = decimal_to_octal(decimal)
    octal_from_hex = hex_to_octal(hex_string)
    
    print(f"Decimal: {decimal}")
    print(f"Hexadecimal: {hex_string}")
    print(f"Octal (direct conversion): {octal_string}")
    print(f"Octal (via hexadecimal): {octal_from_hex}")


if __name__ == "__main__":
    main()