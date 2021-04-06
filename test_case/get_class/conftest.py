
import pytest

@pytest.fixture(scope='session')
def pub_data():
    data={}
    yield data
