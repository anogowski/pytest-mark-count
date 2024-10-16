#############################################
#	Dual License: BSD-3-Clause AND MPL-2.0	#
#	Copyright (c) 2024, Adam Nogowski		#
#############################################

import logging
import pytest
from pytest import Pytester

default_ini_file: str = """
markers = ["it", "rt", "vt"]
"""

single_test_file: str = "test_single.py"

multi_test_file: str = "test_multi.py"


def test_help_message(pytester: Pytester):
	result = pytester.runpytest('--help',)
	# fnmatch_lines does an assertion internally
	result.stdout.fnmatch_lines([
	    'mark-count:',
	    '*--count-marker=COUNT_MARKERS*Set markers to count (Space Delimited). Will automatically report unique tests. ex: "it vt"',
	])


def test_count_it(pytester: Pytester):
	"""Make sure that pytest accepts our fixture."""
	pytester.makeini(default_ini_file)

	# create a temporary pytest test module
	pytester.copy_example(single_test_file)

	# run pytest with the following cmd args
	result = pytester.inline_run('--mark-count="it"', '-v')
	reports = result.getreports("pytest_runtest_logreport")

	print(reports)
	logging.info(reports)

	# make sure that we get a '0' exit code for the testsuite
	assert result.ret == 0


def test_count_single_it_vt(pytester: Pytester):
	"""Make sure that pytest accepts our fixture."""
	pytester.makeini(default_ini_file)

	# create a temporary pytest test module
	pytester.copy_example(single_test_file)

	# run pytest with the following cmd args
	result = pytester.inline_run('--mark-count="it vt"', '-v')
	reports = result.getreports("pytest_runtest_logreport")

	print(reports)
	logging.info(reports)

	# make sure that we get a '0' exit code for the testsuite
	assert result.ret == 0


def test_count_multi_it_vt(pytester: Pytester):
	"""Make sure that pytest accepts our fixture."""
	pytester.makeini(default_ini_file)

	# create a temporary pytest test module
	pytester.makepyfile(multi_test_file)

	# run pytest with the following cmd args
	result = pytester.inline_run('--mark-count="it vt"', '-v')
	reports = result.getreports("pytest_runtest_logreport")

	print(reports)
	logging.info(reports)

	# make sure that we get a '0' exit code for the testsuite
	assert result.ret == 0
