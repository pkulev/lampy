import pytest

from lampylib import Launchpad


# TODO: mock midi ports
@pytest.mark.xfail
def test_connect():
    """Tests for Launchpad.connect() method."""

    lp = Launchpad()

    assert lp == lp.connect()
    assert lp.input.is_port_open() is True
    assert lp.output.is_port_open() is True
