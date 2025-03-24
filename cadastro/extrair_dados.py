from pandas import concat, DataFrame, read_excel

from cadastro import DADOS_EXCEL, MESES

_cadastros: DataFrame | None = None

def _normalizar_dados(dados: DataFrame) -> None:
    '''Esta função normaliza os dados de cadastro, deixando todo o texto em maiúsculo e removendo espaços em branco.'''
    for coluna in dados.columns:
        if dados[coluna].dtype == 'object':
            dados[coluna] = dados[coluna].str.upper().str.strip()

def extrair_dados() -> DataFrame:
    '''Esta função extrai os dados de cadastro de todos os meses e retorna um DataFrame com todos os dados.'''
    global _cadastros
    
    if _cadastros is not None:
        return _cadastros
    
    aux = list()
    header_sheets = ['NOME ', 'APELIDO ', 'ENDEREÇO', 'REFERENCIA', 'CPF', 'TELEFONE']
    for mes in MESES:
        df = read_excel(DADOS_EXCEL, sheet_name=mes, header=6, usecols=header_sheets, names=header_sheets)
        aux.append(df)

    _cadastros = concat(aux, ignore_index=True)
    _normalizar_dados(_cadastros)
    
    return _cadastros

def extrair_dados_completos() -> DataFrame:
    '''Esta função retorna os dados de cadastro que possuem todos os campos preenchidos. Ela remove linhas com campos vazios.'''
    global _cadastros
    
    if _cadastros is None:
        extrair_dados()
    
    return _cadastros.dropna()