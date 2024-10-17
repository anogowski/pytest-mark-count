#############################################
#	Dual License: BSD-3-Clause AND MPL-2.0	#
#	Copyright (c) 2024, Adam Nogowski		#
#############################################

import logging
from typing import Final
from pathlib import Path

import pytest
from pytest import Pytester, RunResult

ROOT_DIR: Final[Path] = Path(__file__).parent.parent.absolute()
EXAMPLE_DIR: Final[Path] = Path(ROOT_DIR / "test_examples")
EXAMPLE_TOML: Final[str] = "pyproject.toml"
EXAMPLE_SINGLE_TEST: Final[str] = "test_single.py"
EXAMPLE_TOML_PATH: Final[Path] = Path(EXAMPLE_DIR / EXAMPLE_TOML)
EXAMPLE_SINGLE_PATH: Final[Path] = Path(EXAMPLE_DIR / EXAMPLE_SINGLE_TEST)


def test_help_messages(pytester: Pytester):
	"""Test the help message of count-marker command."""
	result: RunResult = pytester.runpytest('--help',)
	# fnmatch_lines does an assertion internally
	result.stdout.fnmatch_lines([
	    'mark-count:',
	    '*--mark-count=COUNT_MARKERS*',
	    '*Set markers to count (Space Delimited).*',
	    '*Reports marked, unmarked, unique, and total tests.*',
	    '*ex: --marker-count="it vt"*',
	])
	result.stdout.fnmatch_lines([
	    'mark-count:',
	    '*--mark-count-sep=SEPARATE_MARKERS*',
	    '*Separate markers dict into individual metadata keys*',
	    '*ex: --marker-count-sep=False*',
	])


def test_collect_no_search_markers(pytester: Pytester):
	"""Test the --collect-only command report."""
	# create a temporary pyproject.toml
	toml_path: Path = pytester.makefile(ext=".toml", pyproject=DEFAULT_TOML_FILE)

	# create a temporary pytest test module
	test_path: Path = pytester.makepyfile(test_single=SINGLE_MARK_FILE)

	# run pytest with the following cmd args
	result: RunResult = pytester.runpytest('--collect-only', f'-c "{toml_path}"', test_path)
	logging.info(f"result.stdout:\n{result.stdout}")
	result.stdout.fnmatch_lines(
	    ['*collected 4 items*', r'*Mark-Count: {total_found_items: 4, marked_found_items: 3, unmarked_found_items: 1, single_marked_found_items: 3, multi_marked_found_items: 0, unique_marked_searched_items: 0, single_marked_searched_items: 0, multi_marked_searched_items: 0}*'])

	logging.info(f"EXAMPLE_DIR: {EXAMPLE_DIR}")


def test_collect_search_it_marker(pytester: Pytester):
	"""Test the --collect-only command report."""

	# # create a temporary pyproject.toml
	# toml_path: Path = pytester.makefile(ext=".toml", pyproject=DEFAULT_TOML_FILE)
	toml_path: Path = pytester.copy_example(EXAMPLE_TOML)

	# # create a temporary pytest test module
	# test_path: Path = pytester.makepyfile(test_single=SINGLE_MARK_FILE)
	test_path: Path = pytester.copy_example(EXAMPLE_SINGLE_TEST)

	# run pytest with the following cmd args
	CMD: Final[str] = f'--collect-only --mark-count="it" {test_path}'
	result: RunResult = pytester.runpytest(CMD)

	logging.info(f"result.stdout:\n{result.stdout}")
	# result.stdout.fnmatch_lines(
	#     ['*collected 4 items*', r"*Mark-Count: {total_found_items: 4, marked_found_items: 3, unmarked_found_items: 1, single_marked_found_items: 3, multi_marked_found_items: 0, unique_marked_searched_items: 1, single_marked_searched_items: 1, multi_marked_searched_items: 0, 'it': 1}*"])


def test_count_it(pytester: Pytester):
	"""Test --mark-count="it"."""
	# create a temporary pyproject.toml
	toml_path: Path = pytester.makefile(ext=".toml", pyproject=DEFAULT_TOML_FILE)

	# create a temporary pytest test module
	pytester.makepyfile(test_single=SINGLE_MARK_FILE)

	# run pytest with the following cmd args
	result: RunResult = pytester.runpytest('--mark-count="it"')
	result.stdout.fnmatch_lines("*'it': 1*")

	print(result.stdout)
	logging.info(f"result.stdout:\n{result.stdout}")

	# make sure that we get a '0' exit code for the testsuite
	assert result.ret == 0


def test_count_single_it_vt(pytester: Pytester):
	"""Test --mark-count="it vt"."""
	# create a temporary pyproject.toml
	toml_path: Path = pytester.makefile(ext=".toml", pyproject=DEFAULT_TOML_FILE)
	# create a temporary pytest test module
	pytester.makepyfile(test_single=SINGLE_MARK_FILE)

	# run pytest with the following cmd args
	result = pytester.inline_run('-m "it or vt"', '--mark-count="it vt"', f'-c {toml_path}')
	reports = result.getreports("pytest_runtest_logreport")

	logging.info(reports)

	# make sure that we get a '0' exit code for the testsuite
	assert result.ret == 0


def test_count_multi_it_vt(pytester: Pytester):
	"""Test --mark-count="it vt"."""
	# create a temporary pyproject.toml
	toml_path: Path = pytester.makefile(ext=".toml", pyproject=DEFAULT_TOML_FILE)

	# create a temporary pytest test module
	pytester.makepyfile(test_multi=MULTI_MARK_FILE)

	# run pytest with the following cmd args
	result = pytester.inline_run('--collect-only', '--mark-count="it vt"', '-v')
	reports = result.getreports("pytest_collectreport")

	logging.info(reports)

	# make sure that we get a '0' exit code for the testsuite
	assert result.ret == 0


#FILES

DEFAULT_TOML_FILE: Final[str] = """
[tool.pytest.ini_options]
markers = [
	"it: Integration Tests",
	"rt: Regression Tests",
	"vt: Verification Tests",]
addopts = "--collect-only"
"""

SINGLE_MARK_FILE: Final[str] = """
import pytest

def test_unmarked_pass():
	assert True, "Failed"

@pytest.mark.it
def test_it_pass():
	assert True, "Failed"

@pytest.mark.rt
def test_rt_pass():
	assert True, "Failed"

@pytest.mark.vt
def test_vt_pass():
	assert True, "Failed"
"""

MULTI_MARK_FILE: Final[str] = """
import pytest

def test_unmarked_pass():
	assert True, "Failed"

def test_unmarked_pass_2():
	assert True, "Failed"

@pytest.mark.it
def test_it_pass():
	assert True, "Failed"

@pytest.mark.it
def test_it_pass_2():
	assert True, "Failed"

@pytest.mark.rt
def test_rt_pass():
	assert True, "Failed"

@pytest.mark.rt
def test_rt_pass_2():
	assert True, "Failed"

@pytest.mark.vt
def test_vt_pass():
	assert True, "Failed"

@pytest.mark.vt
def test_vt_pass_2():
	assert True, "Failed"

@pytest.mark.it
@pytest.mark.vt
def test_it_vt_pass():
	assert True, "Failed"

@pytest.mark.it
@pytest.mark.rt
def test_it_rt_pass():
	assert True, "Failed"
"""
