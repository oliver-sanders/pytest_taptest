import shlex
import subprocess

from pytest import main


PARSER_CMDS = {
    'prove': 'prove --exec cat',
    'tappy': 'tappy'
}

TESTS = {
    'test/good.t': 0,
    'test/bad.t': 1,
    'test/ugly.t': 1
}


def get_parsers():
    """Yield valid TAP parser commands."""
    for parser, command in PARSER_CMDS.items():
        if not subprocess.call(['which', shlex.quote(parser)]):
            yield command


PARSERS = [cmd for cmd in get_parsers()]


def test_parsers():
    """ Ensure tests don't become placebos."""
    assert len(PARSERS) >= 1


def test_basic():
    """Test basic usage against all parsers."""
    for parser in PARSERS:
        for test, result in TESTS.items():
            assert main([
                '--tap-test-scripts', '*.t',
                '--tap-parser', parser,
                shlex.quote(test),
            ]) == result


def test_collection():
    """Test that pytest collects only the specified files in globs."""
    for test, result in TESTS.items():
        assert main([
            '--tap-test-scripts', shlex.quote(test),
            '--tap-parser', PARSERS[0],
            'test/'
        ]) == result


def test_environment():
    """Test the sourcing of environment scripts."""
    assert main([
        '--tap-test-scripts', '*.t',
        '--tap-parser', PARSERS[0],
        '--tap-env-script', shlex.quote('test/environment'),
        shlex.quote('test/env.t')
    ]) == 0
