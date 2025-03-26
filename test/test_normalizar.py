import pytest

from pandas import DataFrame
from numpy import nan

from cadastro import NormalizarXl

@pytest.fixture
def dados():
    header_sheets = ['NOME', 'APELIDO', 'ENDEREÇO', 'REFERENCIA', 'CPF', 'TELEFONE']
    return DataFrame(
        {
            1: '''RONALDO JOSÉ MARIANO
            LUANNE DA SILVA MARTINS
            MÁRCIO AGUIAR DA SILVA
            '''.split(),
            2: [nan, nan, nan],
            3: '''SÍTIO AGOSTINHO
            SITIO CACHOEIRA DO SALOBRO
            SITIO TANQUE VERDE
            '''.split(),
            4: '''PROX A FÁBRICA DE VENENO
            AO LADO DO CAMPO
            PROX AO SIT DE PEDRO CABRAL NO CASARÃO
            '''.split(),
            5: '''117.527.524-73
            131.411.584-79
            833.126.094-53
            '''.split(),
            6:'''99282-2899
            99571-8384
            98972-0778
            '''.split()
        }, columns=header_sheets
    )

@pytest.fixture
def norm(dados):
    return NormalizarXl(dados)

def test_todas_normalizacoes(norm: NormalizarXl):
    norm.normalizar()

    tratados = norm.dados_normalizados

    assert tratados['APELIDO'].notna().all(), 'Há dados faltantes na coluna APELIDOS'
    assert tratados['ENDEREÇO'].str.match(), 'Há ENDEREÇOS inconsistentes com o padrão estabelecido'
    # assert tratados['REFERENCIA']
    assert tratados['CPF'].str.match().all(), 'Há CPFs inválidos'
    assert tratados['TELEFONE'].str.match().all(), 'Há TELEFONES inválidos'


