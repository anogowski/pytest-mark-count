#############################################
#	Dual License: BSD-3-Clause AND MPL-2.0	#
#	Copyright (c) 2024, Adam Nogowski		#
#############################################

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
