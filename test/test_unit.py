from pathlib import Path
from pandas import DataFrame


def test_dados_excel():
    from cadastro import DADOS_EXCEL

    assert DADOS_EXCEL.as_posix() == Path(r'C:\Users\Estudos\Documents\cadastro_sec\dados\abastecimento_2024.xlsx').as_posix()

def test_output_excel():
    from cadastro import DADOS_OUTPUT

    assert DADOS_OUTPUT.as_posix() == Path(r'C:\Users\Estudos\Documents\cadastro_sec\dados\cadastros.xlsx').as_posix()

def test_extrair_dados():
    from cadastro import extrair_dados

    dados = extrair_dados()
    
    assert isinstance(dados, DataFrame), 'Os dados extraídos não são um DataFrame'
    assert dados.empty is True, 'Os dados extraídos estão vazios'

def test_extrair_dados_completos():
    from cadastro import extrair_dados_completos

    dados = extrair_dados_completos()

    assert dados.notna().all().all() is True, 'Ainda existem dados faltando'