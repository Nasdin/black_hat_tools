from functools import partial

alphabet = 'abcdefghijklmnopqrstuvwxyz'
alphabet_dict = {letter: order + 1 for order, letter in enumerate(alphabet)}
alphabet_dict_reversed = {order: letter for letter, order in alphabet_dict.items()}


def encrypt_text(text: str, shift: int, decrypt: bool = False):
    shift_n = (shift * (-1 if decrypt else 1))  # Useful line to switch to decryption
    encrypted_text = [
        alphabet_dict_reversed[((alphabet_dict[letter] + shift_n - 1) % 26 + 1)] if alphabet_dict.get(letter,
                                                                                                      False) else letter
        for
        letter in text.lower()]
    return "".join(encrypted_text)


#  A function called decrypt_text to reverse it
decrypt_text = partial(encrypt_text, decrypt=True)

# Tests
if __name__ == '__main__':
    test = "this is a test"
    print(test)
    print("Encrypting test")
    enc1 = (encrypt_text(test, 5))
    enc2 = (encrypt_text(test, 28))  # Can accept shifts more than 26 by going 1 circle
    print(enc1)
    print(enc2)
    print("\nSecond test")
    test2 = "this is test number 2 has % special numbers 123"
    print(test2)
    enc3 = encrypt_text(test2, 24)
    print(enc3)
    print("Decrypting the two test, given the right keys")
    print(decrypt_text(enc1, 5))
    print(decrypt_text(enc2, 28))
    print(decrypt_text(enc3, 24))

    print("\nWhen decryption key is wrong:")
    print(decrypt_text(enc3, 25))

    # Outputs:
    # this is a test
    # Encrypting test
    # ymnx nx f yjxy
    # vjku ku c vguv
    #
    # Second test
    # this is test number 2 has % special numbers 123
    # rfgq gq rcqr lskzcp 2 fyq % qncagyj lskzcpq 123
    # Decrypting the two test, given the right keys
    # this is a test
    # this is a test
    # this is test number 2 has % special numbers 123
    #
    # When decryption key is wrong:
    # sghr hr sdrs mtladq 2 gzr % rodbhzk mtladqr 123
