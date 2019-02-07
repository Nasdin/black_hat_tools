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
    test1 = "If he had anything confidential to say, he wrote it in cipher, that is, by so changing the order of the letters of the alphabet, that not a word could be made out."
    encrypted = encrypt_text(test1, 7)
    assert encrypted == "pm ol ohk hufaopun jvumpkluaphs av zhf, ol dyval pa pu jpwoly, aoha pz, if zv johunpun aol vykly vm aol slaalyz vm aol hswohila, aoha uva h dvyk jvbsk il thkl vba."
    decrypted = decrypt_text(encrypted, 7)
    assert (test1.lower() == decrypted)
