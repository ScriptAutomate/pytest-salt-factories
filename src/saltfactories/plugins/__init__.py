"""
saltfactories.plugins
~~~~~~~~~~~~~~~~~~~~~

Salt Factories PyTest plugin interface
"""
import logging
import os
import sys
import tempfile

import pytest

import saltfactories.utils.tempfiles

log = logging.getLogger(__name__)


def pytest_tempdir_temproot():
    # Taken from https://github.com/saltstack/salt/blob/v2019.2.0/tests/support/paths.py
    # Avoid ${TMPDIR} and gettempdir() on MacOS as they yield a base path too long
    # for unix sockets: ``error: AF_UNIX path too long``
    # Gentoo Portage prefers ebuild tests are rooted in ${TMPDIR}
    if not sys.platform.startswith("darwin"):
        tempdir = os.environ.get("TMPDIR") or tempfile.gettempdir()
    else:
        tempdir = "/tmp"
    return os.path.abspath(os.path.realpath(tempdir))


def pytest_tempdir_basename():
    """
    Return the temporary directory basename for the salt test suite.
    """
    return "saltfactories"


def pytest_runtest_logstart(nodeid):
    """
    signal the start of running a single test item.

    This hook will be called **before** :func:`pytest_runtest_setup`, :func:`pytest_runtest_call` and
    :func:`pytest_runtest_teardown` hooks.

    :param str nodeid: full id of the item
    :param location: a triple of ``(filename, linenum, testname)``
    """
    log.debug(">>>>>>> START %s >>>>>>>", nodeid)


def pytest_runtest_logfinish(nodeid):
    """
    signal the complete finish of running a single test item.

    This hook will be called **after** :func:`pytest_runtest_setup`, :func:`pytest_runtest_call` and
    :func:`pytest_runtest_teardown` hooks.

    :param str nodeid: full id of the item
    :param location: a triple of ``(filename, linenum, testname)``
    """
    log.debug("<<<<<<< END %s <<<<<<<", nodeid)


@pytest.hookimpl(trylast=True)
def pytest_load_initial_conftests(*_):
    """
    Register our pytest helpers
    """
    if "temp_directory" not in pytest.helpers:
        pytest.helpers.register(saltfactories.utils.tempfiles.temp_directory, name="temp_directory")
    if "temp_file" not in pytest.helpers:
        pytest.helpers.register(saltfactories.utils.tempfiles.temp_file, name="temp_file")
