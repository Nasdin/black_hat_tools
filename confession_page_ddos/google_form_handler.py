import urllib.request

import requests
from bs4 import BeautifulSoup


def get_questions(in_url, refresh_counter=1000):
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

        self._confession = ""
        self._matriculation = ""
        self._confession_key = ""
        self.matriculation_key = ""

        self._get_matriculation_form()
        self._get_confession_form()

    def output(self):

        out = {}
        out.update(self.confession)
        out.update(self.matriculation)
        return out

    @property
    def confession(self):

        return {self._confession_key: self._confession}

    @confession.setter
    def confession(self, confess):

        self._confession = confess

    @property
    def matriculation(self):

        return {self._matriculation_key: self._matriculation}

    @matriculation.setter
    def matriculation(self, matriculate):

        self._matriculation = matriculate

    def _get_confession_form(self):

        for i, v in self.raw_dict.items():
            if 'confession' in i.lower():
                self._confession_key = self.raw_dict.pop(i)
                break

    def _get_matriculation_form(self):

        for i, v in self.raw_dict.items():
            if 'matriculation' in i.lower():
                self._matriculation_key = self.raw_dict.pop(i)
                break


def submit_response_factory(form_url, questions_generator, verbose=False):
    submit_url = form_url.replace('/viewform', '/formResponse')
    form_data = {'draftResponse': [],
                 'pageHistory': 0}

    user_agent = {'Referer': form_url,
                  'User-Agent': "Python"}

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
