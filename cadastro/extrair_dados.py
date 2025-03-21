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
        df = read_excel(DADOS_EXCEL, sheet_name=mes, header=6, usecols='A:F', names=header_sheets)
        aux.append(df)

    _cadastros = concat(aux, ignore_index=True)
    
    return _cadastros

cad_completos = _cadastros.dropna()
cad_completos.to_excel(DADOS_EXCEL.parent.joinpath('cadastros.xlsx'), 'CADASTRO_GERAL',startrow=2, index=False)