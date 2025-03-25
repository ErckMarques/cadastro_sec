import pytest

from cadastro import NormalizarXl
from cadastro import ExtratorDadosCadastro

@pytest.fixture(scope='module')
def dados_completos():
    extrator = ExtratorDadosCadastro()
    extrator.extrair_dados_completos()
    return extrator.cadastros_completos

@pytest.fixture(scope='module')
def normalizador(dados_completos):
    return NormalizarXl(dados_completos)

def test_normalizar_telefone():
    pass