from pandas import concat, DataFrame, read_excel

from cadastro import DADOS_EXCEL, DADOS_OUTPUT, MESES

_cadastros: DataFrame | None = None
_cadastros_completos = DataFrame | None = None
_header_sheets = ['NOME ', 'APELIDO ', 'ENDEREÇO', 'REFERENCIA', 'CPF', 'TELEFONE']

def extrair_dados() -> DataFrame:
    global _cadastros
    global _header_sheets

    if _cadastros is not None:
        return _cadastros
    
    aux = list()
    for mes in MESES:
        df = read_excel(DADOS_EXCEL, sheet_name=mes, header=6, usecols=_header_sheets, names=_header_sheets)
        aux.append(df)

    _cadastros = concat(aux, ignore_index=True)
    
    return _cadastros

def extrair_dados_completos(export: bool = True) -> DataFrame:
    global _cadastros
    global _cadastros_completos
    global _header_sheets

    if _cadastros is not None:
        extrair_dados()
    
    _cadastros_completos = _cadastros.dropna()
    
    if export:
        _cadastros_completos.to_excel(DADOS_OUTPUT, sheet_name='CADASTRO_GERAL', startrow=2, index=False)

    return _cadastros_completos

    
    
