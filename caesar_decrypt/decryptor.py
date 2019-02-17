from functools import partial
from itertools import chain

from caesar_cypher import encrypt_text


def training_data_generator(source_text_file: str, max_char: int):
    with open(source_text_file, 'rb', ) as f:
        text_data = f.readlines()
    text_data = (text.decode('utf-8').replace('\n', '') for text in text_data if text is not '\n')
    encrypt_functions = [partial(encrypt_text, shift=shift) for shift in range(0, 26)]
    arguments = chain.from_iterable(
        map(lambda text: ([text[i:i + max_char]] * 26 for i in range(0, len(text), max_char)), text_data))

    yield from ((encrypt_function(arg), shift) for argument in arguments for shift, (arg, encrypt_function) in
                enumerate(zip(argument, encrypt_functions)))






class caesar_decryptor(object):


    def crack(self) -> dict:
        """
        Take an encrypted phrase, predict it, get candidates, then crack it, showing all the possible conversions


        :return:
        """


        pass

    def decrypt(self) -> str:
        """
        Takes either a file path or string.
        decrypts a text
        :return:
        """


        pass

    def save(self):
        pass

    def load(self):
        pass

    def train(self):
        pass

    def predict(self):
        pass