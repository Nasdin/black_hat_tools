SOURCE_TEXT_FILE = 'source_text.txt'

with open(SOURCE_TEXT_FILE, 'r') as f:
    text_data = f.readlines()
    text_data = [text.replace('\n', '') for text in text_data if text is not '\n']

text_data_generator