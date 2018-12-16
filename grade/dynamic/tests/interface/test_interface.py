import json
import pytest

import kutils
from mock import MockQuestion


class TestInterface(object):


    def test_get_question_by_name(self):
        cls = kutils.KQuestionBase.get_subclass_by_name(
            'Mock Question')
        assert cls == MockQuestion


    def test_generate_question(self):
        question = MockQuestion.generate_question()
        form = json.loads(question.output_json)
        assert form['description'] == question.description
        assert form['data'] == question.dumps()


    def test_reconstruction(self):
        old_question = MockQuestion.generate_question()
        form = json.loads(old_question.output_json)
        metadata = dict()
        metadata['on_start'] = onstart = dict()
        onstart['data'] = form['data']
        jstr = json.dumps(metadata)
        new_question = MockQuestion.from_metadata(
            json.loads(jstr))

        assert old_question.first == new_question.first
        assert old_question.second == new_question.second


    def test_solution(self):
        question = MockQuestion((2,3))
        assert question.solution == 5


    def test_score_submission(self):
        question = MockQuestion((2,3))

        submissions = ('5', '05 ', '6', 'I dont know')

        scores = map(question.output_submission, submissions)
        
        def get_score(jstr):
            d = json.loads(jstr)
            return d['score']

        assert (list(map(get_score, scores))
                == [10, 10, 0, 0])
