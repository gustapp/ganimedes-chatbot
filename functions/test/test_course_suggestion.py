import os
import tempfile

import pytest

@pytest.fixture
def client():
    cdn = 5

def test_get_course_suggestion(client):
    """ Course recommendation """
    
    rv = client.get('/course_suggestion')
    assert b'Hello World' in rv.data