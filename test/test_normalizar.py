import pytest

from cadastro import NormalizarXl

@pytest.fixture
def normalizador():
    return NormalizarXl(dados=None)