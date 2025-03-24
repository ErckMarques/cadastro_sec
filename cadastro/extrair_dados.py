from pandas import concat, DataFrame, read_excel

from cadastro import DADOS_EXCEL, MESES

_cadastros: DataFrame | None = None

def extrair_dados() -> DataFrame:
    global _cadastros
    
    if _cadastros is not None:
        return _cadastros
    
    aux = list()
    header_sheets = ['NOME ', 'APELIDO ', 'ENDEREÇO', 'REFERENCIA', 'CPF', 'TELEFONE']
    for mes in MESES:
        df = read_excel(DADOS_EXCEL, sheet_name=mes, header=6, usecols=header_sheets, names=header_sheets)
        aux.append(df)

    _cadastros = concat(aux, ignore_index=True)
    
    return _cadastros

def extrair_dados_completos():
    global _cadastros

    if _cadastros is not None:
        extrair_dados()

    return _cadastros.dropna()