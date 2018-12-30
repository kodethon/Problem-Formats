import kutils
from kutils.parser.core import KParser

class IntegerParser(KParser):

    def __init__(self):
        self._err_msg = 'Input has to be an interger!'
    
    def __call__(self, submission):
        submission = submission.strip().lower()
        try:
            fvalue = float(submission)
            ivalue = int(fvalue)
            if ivalue == fvalue:
                return ivalue
            else:
                raise kutils.InvalidInput(self._err_msg)
        except ValueError:
            raise kutils.InvalidInput(self._err_msg)
