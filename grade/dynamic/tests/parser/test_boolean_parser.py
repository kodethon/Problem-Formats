import pytest

import kutils

class TestBooleanParser(object):

    def test_parse(self):
        parser = kutils.BooleanParser()
        assert parser('Y') == True
        assert parser('YES') == True
        assert parser('y') == True
        assert parser('yes') == True
        assert parser('Yes') == True
        assert parser(' Yes ') == True
        
        assert parser('N') == False
        assert parser('NO') == False
        assert parser('n') == False
        assert parser('no') == False
        assert parser('No') == False
        assert parser(' No ') == False

    def test_invalid(self):
        parser = kutils.BooleanParser()
        with pytest.raises(kutils.InvalidInput):
            parser('I don\'t know.')
