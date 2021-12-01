import pytest

def pytest_addoption(parser):
    parser.addoption("--host", action="store", default="http://127.0.0.1:8000")


@pytest.fixture
def host(request):
    return request.config.getoption('--host')