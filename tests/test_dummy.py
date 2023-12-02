import pytest

from parma_mining.affinity import __version__


@pytest.mark.parametrize("arg", [True, False])
def test_dummy(arg: bool):
    assert arg or not arg
    assert len(__version__) > 0