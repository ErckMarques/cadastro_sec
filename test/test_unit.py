from pathlib import Path

def test_dados_excel():
    from cadastro import DADOS_EXCEL

    assert DADOS_EXCEL.as_posix() == Path(r'C:\Users\Estudos\Documents\cadastro_sec\dados\abastecimento_2024.xlsx').as_posix()

def test_output_excel():
    from cadastro import DADOS_OUTPUT

    assert DADOS_OUTPUT.as_posix() == Path(r'C:\Users\Estudos\Documents\cadastro_sec\dados\cadastros.xlsx').as_posix()

def test_extrair_dados():
    from cadastro import extrair_dados
    from pandas import DataFrame

    dados = extrair_dados()
    
    assert isinstance(dados, DataFrame), 'Os dados extraídos não são um DataFrame'
    assert dados.shape[0] > 0, 'Os dados extraídos estão vazios'

