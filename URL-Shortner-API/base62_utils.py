import string

# Define the character set for Base62
BASE62_ALPHABET = string.digits + string.ascii_letters

def base62_encode(hex_num):
    number = int(hex_num, 16)
    """Encodes an integer into a Base62 string."""
    if number == 0:
        return BASE62_ALPHABET[0]

    base62 = []
    base = len(BASE62_ALPHABET)
    while number:
        number, remainder = divmod(number, base)
        base62.append(BASE62_ALPHABET[remainder])

    return ''.join(reversed(base62))

def base62_decode(base62_string):
    """Decodes a Base62 string into an integer."""
    base = len(BASE62_ALPHABET)
    number = 0

    for char in base62_string:
        number = number * base + BASE62_ALPHABET.index(char)

    return number

# Example usage
if __name__ == "__main__":
    num = 12345
    encoded = base62_encode(num)
    decoded = base62_decode(encoded)

    print(f"Original number: {num}")
    print(f"Encoded Base62: {encoded}")
    print(f"Decoded number: {decoded}")
