def rotl8(x, shift):
    """Rotate left an 8-bit integer x by shift positions."""
    return ((x << shift) & 0xFF) | (x >> (8 - shift))

def multiply_in_gf(a, b, mod_poly):
    """Multiply two numbers in GF(2^8) using a given modulus polynomial."""
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x100:
            a ^= mod_poly
        b >>= 1
    return result & 0xFF

def find_multiplicative_inverse(x, mod_poly):
    """Find the multiplicative inverse of x in GF(2^8) defined by mod_poly."""
    if x == 0:
        return 0
    for i in range(1, 256):
        if multiply_in_gf(x, i, mod_poly) == 1:
            return i
    return 0  # Should never happen for valid GF(2^8)

def generate_sbox_and_inverse(mod_poly, constant):
    """Generate the S-Box and its inverse for a given mod_poly and constant."""
    sbox = [0] * 256
    inv_sbox = [0] * 256

    for i in range(256):
        inverse = find_multiplicative_inverse(i, mod_poly)

        if inverse == 0:
            sbox[i] = constant
        else:
            # AES-like transformation on the inverse
            xformed = (inverse ^ rotl8(inverse, 1) ^ rotl8(inverse, 2) ^ rotl8(inverse, 3) ^ rotl8(inverse, 4))
            sbox[i] = xformed ^ constant

        # Ensure the S-Box value maps correctly to its inverse
        inv_sbox[sbox[i]] = i

    return sbox, inv_sbox

def print_sbox(sbox, title):
    """Print the S-Box or inverse S-Box."""
    print(f"{title}:")
    for i in range(0, 256, 16):
        print(" ".join(f"{x:02X}" for x in sbox[i:i+16]))
    print()

# Test with the provided polynomial and constant
mod_poly = 0x11D  # Polynomial (GF(2^8) modulus)
constant = 0x63  # Additive constant used in AES

sbox, inv_sbox = generate_sbox_and_inverse(mod_poly, constant)
print_sbox(sbox, "S-Box")
print_sbox(inv_sbox, "Inverse S-Box")
