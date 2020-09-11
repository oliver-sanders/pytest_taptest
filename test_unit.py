"""Unit tests of python code."""
from pytest_taptest import (
    get_environment
)


def test_get_environment(tmp_path):
    script = tmp_path / 'script'
    with open(script, 'w+') as script_file:
        script_file.write('''
            export ANSWER=42
        ''')
    env = get_environment(str(script))
    assert env['ANSWER'] == '42'
