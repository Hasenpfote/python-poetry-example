import platform
import sys

from python_poetry_example import utils


def test_add():
    assert utils.add(1, 2) == 3


def test_print_greet(capfd):
    utils.print_greet()

    out, err = capfd.readouterr()
    assert out == 'Hello, world!\n'
    assert err == ''


def test_print_mascot(capfd):
    utils.print_mascot()

    d = {'Linux': 'Tux', 'Darwin': 'Dogcow'}
    name = d.get(platform.system(), 'Unknown')

    out, err = capfd.readouterr()
    assert out == name + '\n'
    assert err == ''


def test_is_py38_or_higher():
    is_py38_or_higher = False if sys.version_info < (3, 8) else True
    assert utils.is_py38_or_higher() == is_py38_or_higher


def test_print_python_version(capfd):
    utils.print_python_version()

    out, err = capfd.readouterr()
    assert out != ''
    assert err == ''


def test_print_with_delay(capfd, mocker):
    m = mocker.patch('python_poetry_example.utils.time.sleep', return_value=None)

    text = 'Hello, world!'
    utils.print_with_delay(text)

    m.assert_called_once_with(len(text) / 100 + 1.0)
    out, err = capfd.readouterr()
    assert out == text + '\n'
    assert err == ''
