import pytest

import kutils

class TestIntegerParser(object):

    def test_parse(self):
        parser = kutils.IntegerParser()
        inputs = ('-1', '0', '1', '1.2e2', '-1.0')
        outputs = (-1, 0, 1, 120, -1)
        assert list(map(parser, inputs)) == list(outputs)
        

    def test_invalid(self):
        inputs = ('I don\'t know.', '-1.2', '1.25e1')
        parser = kutils.IntegerParser()
        for i in inputs:
            with pytest.raises(kutils.InvalidInput):
                parser(i)
