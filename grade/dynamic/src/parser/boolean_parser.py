import kutils
from kutils.parser.core import KParser

class BooleanParser(KParser):

    def __init__(self):
        self._err_msg = 'Input has to be yes or no!'

    def __call__(self, submission):
        submission = submission.strip().lower()
        if submission in ('y','yes'):
            return True
        if submission in ('n','no'):
            return False
        raise kutils.InvalidInput(self._err_msg)
