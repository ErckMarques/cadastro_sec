import pytest
from pathlib import Path
from pandas import DataFrame

from cadastro import extrair_dados, extrair_dados_completos
from cadastro import DADOS_EXCEL, DADOS_OUTPUT

def test_dados_excel():

    assert DADOS_EXCEL.as_posix() == Path().cwd().joinpath('dados', 'abastecimento_2024.xlsx').as_posix()

def test_output_excel():

    assert DADOS_OUTPUT.as_posix() == Path().cwd().joinpath('dados', 'cadastros.xlsx').as_posix()

def test_extrair_dados():

    dados = extrair_dados()
    
    assert isinstance(dados, DataFrame), 'Os dados extraídos não são um DataFrame'
    assert not dados.empty, 'o Dataframe retornado está vazio'

def test_extrair_dados_completos():

    dados = extrair_dados_completos()

    assert dados.notna().all().all(), 'Ainda existem dados faltando'
    assert not dados.duplicated().all(), 'Ainda existem dados duplicados'