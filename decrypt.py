#!/usr/bin/env python3

def base36_encode(num: int) -> str:
    """Convert integer to Base36 string (0-9A-Z)."""
    if num == 0:
        return "0"
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = []
    while num > 0:
        num, rem = divmod(num, 36)
        result.append(chars[rem])
    return ''.join(reversed(result))

def base36_decode(s: str) -> int:
    """Convert Base36 string to integer."""
    return int(s, 36)

def encode_to_hex(message: str, username: str) -> str:
    """Encode message to obfuscated hex."""
    # XOR with repeating key
    msg_bytes = message.encode('utf-8')
    key_bytes = username.encode('utf-8')
    key_repeated = (key_bytes * (len(msg_bytes) // len(key_bytes) + 1))[:len(msg_bytes)]
    xor_bytes = bytes([m ^ k for m, k in zip(msg_bytes, key_repeated)])
    
    # Convert XOR bytes to integer, then to Base36
    xor_int = int.from_bytes(xor_bytes, byteorder='big')
    base36_str = base36_encode(xor_int)
    
    # Return hex of Base36 string
    return base36_str.encode('utf-8').hex()

def decode_from_hex(hex_ciphertext: str, username: str):
    """Decode obfuscated hex back to original."""
    # Hex decode to get Base36 string
    base36_bytes = bytes.fromhex(hex_ciphertext)
    base36_str = base36_bytes.decode('utf-8')
    
    # Base36 decode to integer
    xor_int = base36_decode(base36_str)
    
    # Convert integer to bytes (need exact byte length)
    # For "earth" test: XOR result = 0x04051f1d06 = 5 bytes
    xor_hex = hex(xor_int)[2:]
    if len(xor_hex) % 2:
        xor_hex = '0' + xor_hex
    xor_bytes = bytes.fromhex(xor_hex)
    
    # XOR with key to get plaintext
    key_bytes = username.encode('utf-8')
    key_repeated = (key_bytes * (len(xor_bytes) // len(key_bytes) + 1))[:len(xor_bytes)]
    plain_bytes = bytes([x ^ k for x, k in zip(xor_bytes, key_repeated)])
    
    return plain_bytes.decode('utf-8', errors='replace'), xor_int

# TEST with known example
print("=" * 60)
print("TEST: 'earth' + 'admin'")
print("=" * 60)

known_hex = encode_to_hex("earth", "admin")
print(f"Encoded hex: {known_hex}")
print(f"Expected:    04051f1d06")
print(f"Match:       {known_hex == '04051f1d06'}")

decoded_msg, decoded_int = decode_from_hex(known_hex, "admin")
print(f"Decoded message: {decoded_msg}")
print(f"Decoded int:     {decoded_int}")

# YOUR THREE RIDDLES
ciphertexts = [
    "37090b59030f11060b0a1b4e0000000000004312170a1b0b0e4107174f1a0b044e0a000202134e0a161d17040359061d43370f15030b10414e340e1c0a0f0b0b061d430e0059220f11124059261ae281ba124e14001c06411a110e00435542495f5e430a0715000306150b0b1c4e4b5242495f5e430c07150a1d4a410216010943e281b54e1c0101160606591b0143121a0b0a1a00094e1f1d010e412d180307050e1c17060f43150159210b144137161d054d41270d4f0710410010010b431507140a1d43001d5903010d064e18010a4307010c1d4e1708031c1c4e02124e1d0a0b13410f0a4f2b02131a11e281b61d43261c18010a43220f1716010d40",
    
    "3714171e0b0a550a1859101d064b160a191a4b0908140d0e0d441c0d4b1611074318160814114b0a1d06170e1444010b0a0d441c104b150106104b1d011b100e59101d0205591314170e0b4a552a1f59071a16071d44130f041810550a05590555010a0d0c011609590d13430a171d170c0f0044160c1e150055011e100811430a59061417030d1117430910035506051611120b45",
    
    "2402111b1a0705070a41000a431a000a0e0a0f04104601164d050f070c0f15540d1018000000000c0c06410f0901420e105c0d074d04181a01041c170d4f4c2c0c13000d430e0e1c0a0006410b420d074d55404645031b18040a03074d181104111b410f000a4c41335d1c1d040f4e070d04521201111f1d4d031d090f010e00471c07001647481a0b412b1217151a531b4304001e151b171a4441020e030741054418100c130b1745081c541c0b0949020211040d1b410f090142030153091b4d150153040714110b174c2c0c13000d441b410f13080d12145c0d0708410f1d014101011a050d0a084d540906090507090242150b141c1d08411e010a0d1b120d110d1d040e1a450c0e410f090407130b5601164d00001749411e151c061e454d0011170c0a080d470a1006055a010600124053360e1f1148040906010e130c00090d4e02130b05015a0b104d0800170c0213000d104c1d050000450f01070b47080318445c090308410f010c12171a48021f49080006091a48001d47514c50445601190108011d451817151a104c080a0e5a"
]

print("\n" + "=" * 60)
print("DECODING YOUR THREE RIDDLES")
print("=" * 60)

username = "admin"

for i, hex_cipher in enumerate(ciphertexts, 1):
    print(f"\n{'─' * 50}")
    print(f"Riddle {i}:")
    print(f"Hex (first 40 chars): {hex_cipher[:40]}...")
    try:
        decoded_msg, decoded_int = decode_from_hex(hex_cipher, username)
        print(f"✓ Decoded successfully!")
        print(f"  Message text: {decoded_msg}")
        print(f"  As integer:   {decoded_int}")
        
        # Try interpreting as coordinate
        int_str = str(decoded_int)
        if len(int_str) >= 10:
            lat = f"{int_str[:2]}.{int_str[2:]}"
            print(f"  As latitude:  {lat}° N (if coordinate)")
    except Exception as e:
        print(f"✗ Decoding failed: {e}")