import urllib.request

import requests
from bs4 import BeautifulSoup


def get_questions(in_url: str, refresh_counter: int = 1000):
    """
    Generates questions, refreshes the format and beautiful soup parse every `refresh_counter` in case the page changes
    """
    while True:

        res = urllib.request.urlopen(in_url)
        soup = BeautifulSoup(res.read(), 'html.parser')
        get_names = lambda f: [v for k, v in f.attrs.items() if 'label' in k]
        get_name = lambda f: get_names(f)[0] if len(get_names(f)) > 0 else 'unknown'
        all_questions = soup.form.findChildren(attrs={'name': lambda x: x and x.startswith('entry.')})
        forms = {get_name(q): q['name'] for q in all_questions}

        confession_field = ConfessionField(forms)

        for _ in range(refresh_counter):
            yield confession_field


class ConfessionField(object):

    def __init__(self, google_form_output_dict: dict):
        self.raw_dict = google_form_output_dict.copy()

        self.confession = ""
        self.matriculation = ""
        self._confession_key = ""
        self._matriculation_key = ""

        self._get_matriculation_form()
        self._get_confession_form()

    def output(self):

        return {self._confession_key: self.confession,
                self._matriculation_key: self.matriculation}

    def _get_confession_form(self):
        for description in self.raw_dict.keys():
            if 'confession' in description.lower():
                self._confession_key = self.raw_dict.pop(description)
                return

    def _get_matriculation_form(self):
        for description in self.raw_dict.keys():
            if 'matriculation' in description.lower():
                self._matriculation_key = self.raw_dict.pop(description)
                return


def submit_response_factory(form_url, questions_generator, verbose=False):
    submit_url = form_url.replace('/viewform', '/formResponse')
    form_data = {'draftResponse': [],
                 'pageHistory': 0}

    user_agent = {'Referer': form_url,
                  'User-Agent': "Python"}  # TODO, Spoof multiple User-Agent in case this gets fixed.

    def submit_response(matriculation, confession):
        confession_field = next(questions_generator)

        confession_field.confession = confession
        confession_field.matriculation = matriculation
        out = confession_field.output()

        form_data.update(out)
        if verbose:
            print(form_data)

        return requests.post(submit_url, data=form_data, headers=user_agent)

    return submit_response
