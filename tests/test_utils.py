# https://stackoverflow.com/a/50740647
from unittest.mock import patch

from pyenv_poetry_tox_pytest_example import utils


def test_add():
    assert utils.add(1, 2) == 3


@patch("builtins.print")
def test_print_greet(mock_print):
    utils.print_greet()

    mock_print.assert_called_with('Hello, world!')


@patch("builtins.print")
def test_print_python_version(mock_print):
    utils.print_python_version()

    mock_print.assert_called_once()
