from pandas import DataFrame
from pathlib import Path

from cadastro import extrair_dados, extrair_dados_completos

def test_dados_excel():
    from cadastro import DADOS_EXCEL

    assert DADOS_EXCEL.as_posix() == Path(r'C:\Users\Estudos\Documents\cadastro_sec\dados\abastecimento_2024.xlsx').as_posix()

def test_output_excel():
    from cadastro import DADOS_OUTPUT

    assert DADOS_OUTPUT.as_posix() == Path(r'C:\Users\Estudos\Documents\cadastro_sec\dados\cadastros.xlsx').as_posix()

def test_extrair_dados():

    dados = extrair_dados()
    
    assert isinstance(dados, DataFrame), 'Os dados extraídos não são um DataFrame'
    assert not dados.empty, 'Os dados extraídos estão vazios'

def test_extrair_dados_completos():

    dados = extrair_dados_completos()
    
    assert dados.notna().all().all(), 'Os dados extraídos estão com valores nulos'


