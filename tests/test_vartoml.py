import pytest

from vartoml import VarToml


@pytest.fixture
def vtoml():
    return VarToml()


def test_simple(vtoml):
    """A simple TOML document without any variables

        This works the same as when using the `toml` package
        without any extensions
    """

    tomls_str = """
    [default]

    h = "/home"

    """
    toml = vtoml.loads(tomls_str)
    assert vtoml.get('default', 'h') == '/home'


def test_vartoml1(vtoml):
    """A simple TOML document using variables """

    tomls_str = """

    [default]

    h = "/home"
    m = "${default:h}/manfred"
    b = "${default:m}/bin"

    [other]

    server = "${default:b}/server"
    """

    vtoml.loads(tomls_str)
    assert vtoml.get('other', 'server') == '/home/manfred/bin/server'


def test_vartoml2(vtoml):
    """ test with variable names containing digits, underscores and dashes"""

    tomls_str = """

    [default]

    _h = "/home"
    -m = "${default:_h}/manfred"
    b = "${default:-m}/bin"

    """

    vtoml.loads(tomls_str)
    assert vtoml.get('default', 'b') == '/home/manfred/bin'

def test_nested(vtoml):
    """ test with variable names containing digits, underscores and dashes"""

    tomls_str = """
        [products.food]
        type = "cake"

        [test]
        mytype = "${products:food:type}"
    """

    vtoml.loads(tomls_str)
    assert vtoml.get('test', 'mytype') == "cake"
    assert vtoml.get('products', 'food', 'type') == "cake"


def test_vartoml3(vtoml):
    """ test with variable names containing digits, underscores and dashes"""

    tomls_str = """

    [default]

    1h = "/home"
    -m = "${default:1h}/manfred"
    b = "${default:-m}/bin"

    """

    vtoml.loads(tomls_str)
    assert vtoml.get('default', 'b') == '/home/manfred/bin'
