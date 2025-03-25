from pandas import concat, DataFrame, read_excel

from cadastro import DADOS_EXCEL, DADOS_OUTPUT, MESES

_cadastros: DataFrame | None = None
_cadastros_completos: DataFrame | None = None
_header_sheets = ['NOME', 'APELIDO', 'ENDEREÇO', 'REFERENCIA', 'CPF', 'TELEFONE']

def _normalizar_dados(dados: DataFrame) -> None:
    '''Esta função normaliza os dados de cadastro, deixando todo o texto em maiúsculo e removendo espaços em branco.'''
    for coluna in dados.columns:
        if dados[coluna].dtype == 'object':
            dados[coluna] = dados[coluna].str.upper().str.strip()

def extrair_dados() -> DataFrame:
    '''Esta função extrai os dados de cadastro de todos os meses e retorna um DataFrame com todos os dados.'''
    global _cadastros
    global _header_sheets

    if _cadastros is not None:
        return _cadastros
    
    aux = list()
    for mes in MESES:
        df = read_excel(DADOS_EXCEL, sheet_name=mes, header=6, usecols=_header_sheets, names=_header_sheets)
        aux.append(df)

    _cadastros = concat(aux, ignore_index=True)
    _normalizar_dados(_cadastros)
    
    return _cadastros

def extrair_dados_completos(export: bool = True) -> DataFrame:
    '''Esta função retorna os dados de cadastro completos, ou seja, sem dados faltantes ou duplicados.'''
    global _cadastros
    global _cadastros_completos
    global _header_sheets

    if _cadastros is not None:
        extrair_dados()
    
    _cadastros_completos = _cadastros.dropna().drop_duplicates()

    if export:
        _cadastros_completos.to_excel(DADOS_OUTPUT, sheet_name='CADASTRO_GERAL', startrow=2, index=False)

    return _cadastros_completos

    
    
