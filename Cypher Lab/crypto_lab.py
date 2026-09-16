
def caesar_cipher(message, shift, mode):
    result = ""

    if mode == 'd':
        shift = -shift

    for char in message:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')

            shifted_char = chr(
                (ord(char) - shift_base + shift) % 26 + shift_base
            )

            result += shifted_char
        else:
            result += char

    return result


def atbash_cipher(message):
    result = ""

    for char in message:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')

            shifted_char = chr(
                (25 - (ord(char) - shift_base)) + shift_base
            )

            result += shifted_char
        else:
            result += char

    return result


def vigenere_cipher(message, key, mode):
    result = ""
    key = key.upper()
    key_index = 0

    for char in message:
        if char.isalpha():

            shift_base = ord('A') if char.isupper() else ord('a')

            key_char = key[key_index % len(key)]
            shift_value = ord(key_char) - ord('A')

            if mode == 'e':
                shift = shift_value
            else:
                shift = -shift_value

            shifted_char = chr(
                (ord(char) - shift_base + shift) % 26 + shift_base
            )

            result += shifted_char
            key_index += 1

        else:
            result += char

    return result


def rot13_cipher(message):
    result = ""

    for char in message:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            shifted_char = chr(
                (ord(char) - shift_base + 13) % 26 + shift_base
            )
            result += shifted_char
        else:
            result += char

    return result


def affine_cipher(message, a, b, mode):
    result = ""

    for char in message:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            x = ord(char) - shift_base

            if mode == 'e':
                y = (a * x + b) % 26

            elif mode == 'd':
                a_inverse = pow(a, -1, 26)
                y = (a_inverse * (x - b)) % 26

            result += chr(y + shift_base)

        else:
            result += char

    return result   


def xor_cipher(message, key):
    result = ""

    for char in message:
        result += chr(ord(char) ^ key)

    return result


def rail_fence_encrypt(message, rails):
    if rails <= 1:
        return message

    fence = ['' for _ in range(rails)]
    row = 0
    direction = 1

    for char in message:
        fence[row] += char

        if row == 0:
            direction = 1
        elif row == rails - 1:
            direction = -1

        row += direction

    return ''.join(fence)

def bacon_encrypt(message):
    alphabet = "ABCDEFGHIKLMNOPQRSTUWXYZ"
    result = ""

    for char in message.upper():
        if char in alphabet:
            index = alphabet.index(char)
            binary = format(index, '05b')
            binary = binary.replace('0', 'A').replace('1', 'B')
            result += binary

    return result


# -------------------------------
# CryptoLab
# -------------------------------

print("===== CryptoLab =====")

cipher_type = input(
    "Enter cipher type:\n"
    "'1' for Caesar Cipher\n"
    "'2' for Atbash Cipher\n"
    "'3' for Vigenère Cipher\n"
    "'4' for ROT13 Cipher\n"
    "'5' for Affine Cipher\n"
    "'6' for XOR Cipher\n"
    "'7' for Rail Fence Cipher\n"
    "'8' for Baconian Cipher\n"
    "Choice: "
)

cipher_mode = input(
    "Enter 'e' to encrypt or 'd' to decrypt: "
).lower()

if cipher_mode not in ['e', 'd']:
    print("Invalid mode. Please enter 'e' or 'd'.")

else:
    message = input("Enter your message: ")

    if cipher_type == '1':

        shift = int(input("Enter the shift value: "))

        result = caesar_cipher(message, shift, cipher_mode)

        print("Caesar Cipher Result:", result)

    elif cipher_type == '2':

        result = atbash_cipher(message)

        print("Atbash Cipher Result:", result)

    elif cipher_type == '3':

        key = input("Enter the key for Vigenère Cipher: ")

        if not key.isalpha():
            print("Invalid key. Key must contain letters only.")

        else:
            result = vigenere_cipher(message, key, cipher_mode)

            print("Vigenère Cipher Result:", result)

    elif cipher_type == '4':

        result = rot13_cipher(message)

        print("ROT13 Cipher Result:", result)

    elif cipher_type == '5':

        a = int(input("Enter the value of 'a' for Affine Cipher: "))
        b = int(input("Enter the value of 'b' for Affine Cipher: "))

        result = affine_cipher(message, a, b, cipher_mode)

        print("Affine Cipher Result:", result)

    elif cipher_type == '6':

        key = int(input("Enter the key for XOR Cipher: "))

        result = xor_cipher(message, key)

        print("XOR Cipher Result:", result)

    else:
        print("Invalid cipher type. Please choose 1, 2, 3, 4, 5, 6, 7, or 8.")

