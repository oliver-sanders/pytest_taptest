"""Simple pytest extension for running tests which output TAP files."""
from subprocess import Popen, PIPE, STDOUT
import shlex
from tempfile import NamedTemporaryFile

import pytest


TEST_GLOBALS = {}


def pytest_addoption(parser):
    """Add command line options required by ShellTest."""
    group = parser.getgroup('collect')
    group.addoption(
        '--tap-test-scripts',
        action='append',
        default=[],
        metavar='pattern',
        help='Locate TAP test files.'
    )
    group.addoption(
        '--tap-parser',
        action='store',
        default='tappy',
        help=('Script to pipe TAP output to. Should exit non-zero on test '
              'error.')
    )
    group.addoption(
        '--tap-env-script',
        action='store',
        default=None,
        dest='env_script',
        help=('Executable script, the resulting environment will be used '
              'for all tests.')
    )


def get_environment(script):
    """Source the given script, return a dictionary of the resulting env."""
    out = Popen(
        '( . %s; /usr/bin/printenv -0 )' % script, stdout=PIPE, shell=True
    ).communicate()[0]
    return dict(
        line.decode().split('=', 1) for line in out.split(b'\x00') if line)


def pytest_collectstart(collector):
    """Set custom environment if defined."""
    env_script = collector.config.getoption('env_script')
    if env_script:
        TEST_GLOBALS['env'] = get_environment(env_script)
    TEST_GLOBALS['patterns'] = collector.config.getoption('tap_test_scripts')


def pytest_collect_file(parent, path):
    """Determine which files to test."""
    if any(path.check(fnmatch=glob) for glob in TEST_GLOBALS['patterns']):
        return TAPTestFile(path, parent)
    return None


class TAPTestFile(pytest.File):
    """Represents a script which generates TAP output."""

    def collect(self):
        """Yield test items, there is a 1-1 mapping between files and tests."""
        yield TAPTestItem(self.fspath, self)


class TAPTestFailure(Exception):
    """Exception for error in executing the test or parsing its output."""

    def __str__(self):
        ret = ''
        for name, content in self.args[0].items():
            if content:
                ret += f'\n== {name} ==\n{content}'
        return ret


class TAPTestItem(pytest.Item):
    """Represents a single test in the pytest framework.

    As we cannot determine the test schedule without running the test first
    there is a one-to-one mapping between TAPTestFile and TAPTestItem.
    Normally this would be one-to-many.

    """

    def __init__(self, test_file, parent):
        pytest.Item.__init__(self, 'TAP', parent)
        self.test_file = test_file

    def runtest(self):
        """Execute the test file and run the TAP parser over it."""
        files = {}

        # generate TAP file
        tap_file = NamedTemporaryFile()
        proc = Popen([self.test_file], env=TEST_GLOBALS.get('env'),
                     stdout=tap_file, stderr=PIPE)
        ret = proc.wait()
        tap_file.seek(0)
        files = {
            'TAP File': tap_file.read().decode(),
            'Test Stderr': proc.communicate()[1].decode()
        }
        tap_file.seek(0)
        if ret:
            raise TAPTestFailure(files)

        # parse TAP file
        proc = Popen(
            shlex.split(self.parent.config.getoption('tap_parser'))
            + [tap_file.name],
            stdin=PIPE, stdout=PIPE, stderr=STDOUT
        )
        out = proc.communicate()[0]
        if proc.returncode:
            # important to report parser output e.g. "invalid test plan"
            files['TAP Parser Output'] = out.decode()
            raise TAPTestFailure(files)

    def repr_failure(self, excinfo):
        """Called when runtest raises an exception.

        Returns:
            string - If the exception raised represents a failure in the test
                (i.e. an expected failure).

        """
        ret = None
        if isinstance(excinfo.value, TAPTestFailure):
            ret = str(excinfo.value)
        return ret

    def reportinfo(self):
        """Return the test identifier as it should appear in pytest output."""
        return self.fspath, 0, self.fspath
