import pytest

from pandas import DataFrame, NA
from numpy import nan

from cadastro.normalizar_dados import NormalizarDadosCadastro

@pytest.fixture(scope='module')
def dados():
    """Fixture: Retorna DataFrame de teste com colunas NOME, CPF, TELEFONE, etc."""
    return DataFrame(
        {
            'NOME': ['RONALDO JOSÉ MARIANO', 'LUANNE DA SILVA MARTINS', 'MÁRCIO AGUIAR DA SILVA', 'Ericson Marques'],
            'APELIDO': [nan, nan, nan, 'Eric'],  # Opcional: substituir por ['', '', '']
            'ENDEREÇO': ['SÍTIO AGOSTINHO (PROX A FÁBRICA DE VENENO)', 'SITIO CACHOEIRA DO SALOBRO', 'SITIO TANQUE VERDE', 'Rua das Flores'],
            'REFERENCIA': [nan, 'AO LADO DO CAMPO', 'PROX AO SIT DE PEDRO CABRAL NO CASARÃO', ''],
            'CPF': ['117.527.524-73', '131.411.584-79', '833.126.094-53', '123.456.789-00'],
            'TELEFONE': ['99282-2899', '99571-8384', '98972-0778', '99999-9999']
        }
    )

@pytest.fixture(scope='module')
def norm(dados):
    return NormalizarDadosCadastro(dados)

def test_normalizar_apelido(norm: NormalizarDadosCadastro):
    '''o método cadastro.NormalizarDadosCadastro._normalizar_apelido deve colocar os dois primeiros nomes nas linhas que forem NAN'''
    norm._normalizar_apelido()
    assert norm.dados_normalizados['APELIDO'].isna().all(), 'A normalização da coluna apelidos não foi bem sucedida.'

def test_normalizar_telefone(norm: NormalizarDadosCadastro):
    norm._normalizar_telefone()

@pytest.mark.skip
def test_todas_normalizacoes(norm: NormalizarDadosCadastro):
    norm.normalizar()

    tratados = norm.dados_normalizados

    assert tratados['APELIDO'].notna().all(), 'Há dados faltantes na coluna APELIDOS'
    assert tratados['ENDEREÇO'].str.match(), 'Há ENDEREÇOS inconsistentes com o padrão estabelecido'
    # assert tratados['REFERENCIA']
    assert tratados['CPF'].str.match().all(), 'Há CPFs inválidos'
    assert tratados['TELEFONE'].str.match().all(), 'Há TELEFONES inválidos'


