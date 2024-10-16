import pytest


def test_unmarked_pass():
	assert True, "Failed"


def test_unmarked_fail():
	assert False, "Failed"


@pytest.mark.it
def test_it_pass():
	assert True, "Failed"


@pytest.mark.it
def test_it_fail():
	assert False, "Failed"


@pytest.mark.rt
def test_rt_pass():
	assert True, "Failed"


@pytest.mark.rt
def test_rt_fail():
	assert False, "Failed"


@pytest.mark.vt
def test_vt_pass():
	assert True, "Failed"


@pytest.mark.vt
def test_vt_fail():
	assert False, "Failed"


@pytest.mark.it
@pytest.mark.vt
def test_it_vt_pass():
	assert True, "Failed"
