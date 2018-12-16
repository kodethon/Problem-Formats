import abc
import codecs
import json
import logging
import pickle

import kutils


class KQuestionBase(object):
    """Abstract class for most general Kodethon Questions."""

    __metaclass__ = abc.ABCMeta

    @classmethod
    def get_subclasses(cls):
        for subclass in cls.__subclasses__():
            for sub in subclass.get_subclasses():
                yield sub
            yield subclass


    @classmethod
    def get_subclass_by_name(cls, name):
        for subclass in cls.get_subclasses():
            if '_name' in subclass.__dict__ and subclass._name == name:
                return subclass
            if subclass.__name__ == name:
                return subclass
        raise Exception('There is no class available for {}'.format(name))


    @classmethod
    def from_metadata(cls, metadata):
        try:
            data = metadata['on_start']['data']
        except KeyError as e:
            logging.info('Cannot find specific data from metadata:'
                        + e.message)
            data = None
        return cls.loads(data)


    @staticmethod
    def loads(data):
        """Recover from portable string."""
        return pickle.loads(codecs.decode(data.encode(), "base64"))


    def dumps(self):
        """Serialize self to portable string."""
        return codecs.encode(pickle.dumps(self), "base64").decode()


    def __init__(self):
        self._metadata = dict()


    @property
    def output_json(self):
        output_dict = dict()
        try:
            output_dict.update(self._metadata)
        except AttributeError:
            pass
        output_dict['description'] = self.description
        output_dict['data'] = self.dumps()
        return json.dumps(output_dict, indent=1)


    @abc.abstractproperty
    def description(self):
        pass


    @abc.abstractmethod
    def score_submission(self, submission):
        pass


    def output_submission(self, raw_submission):
        try:
            parser = self.parser
        except AttributeError:
            parser = None

        if parser is None:
            submission = raw_submission
        else:
            try:
                submission = parser(raw_submission)
                score_map = self.score_submission(submission)
            except kutils.InvalidInput as e:
                score_map = kutils.score_map(0, comment=str(e))

        output_dict = dict()
        output_dict['score'] = score_map['score']
        output_dict['output'] = score_map['output']
        return json.dumps(output_dict)


class KQuestion(KQuestionBase):
    """Abstract class for question follow ECS 20 paradigm."""

    @staticmethod
    @abc.abstractmethod
    def generate_question(**gen_args):
        pass


    @abc.abstractproperty
    def solution(self):
        pass
