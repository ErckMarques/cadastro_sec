'''
Este módulo contém a classe NormalizarXl,
que é responsável por normalizar os dados de um arquivo excel com formato já definido.
'''

from pandas import DataFrame, read_excel, concat
from pandas import ExcelWriter, Series
from re import compile, Pattern

class NormalizarXl:
    
    def __init__(self, dados: DataFrame):
        self._dados = dados
        self._column_names = ['NOME', 'APELIDO', 'ENDEREÇO', 'CPF', 'TELEFONE']

    def normalizar_referencia(self):
        '''Esta função normaliza o endereço dos dados de cadastro.'''
        self._dados['ENDEREÇO'] = self._dados['ENDEREÇO'].str.upper().str.strip().str.replace(')', '')
    
    def _normalizar_cpf(self) -> None:
        '''Esta função normaliza o CPF dos dados de cadastro.'''
        
        regex = compile(r'\d{3}\.\d{3}\.\d{3}-\d{2}')

    import pandas as pd
import re

def formatar_telefone(serie_telefone: Series) -> Series:
    """
    Valida e formata a série 'TELEFONE' para o padrão 9XXXX-XXXX,
    adicionando o DDD '81' aos números válidos.

    Args:
        serie_telefone: Série pandas com números de telefone.

    Returns:
        Série com telefones formatados (81 + 9XXXX-XXXX) ou None para inválidos.
    """
    telefones_formatados = []
    
    for telefone in serie_telefone:
        # Converte para string e remove espaços e caracteres especiais
        telefone = str(telefone).strip().replace(' ', '').replace('-', '').replace('.', '')
        
        # Verifica se já está no formato 9XXXX-XXXX
        if re.match(r'^9\d{4}-\d{4}$', telefone):
            telefones_formatados.append(f'81{telefone}')
            continue
        
        # Tenta corrigir números com 9 dígitos (sem hífen)
        if re.match(r'^9\d{8}$', telefone):
            telefone_formatado = f"{telefone[:5]}-{telefone[5:]}"
            telefones_formatados.append(f'81{telefone_formatado}')
            continue
        
        # Tenta corrigir números com 8 dígitos (adiciona o '9' no início)
        if re.match(r'^\d{8}$', telefone):
            telefone_formatado = f"9{telefone[:4]}-{telefone[4:]}"
            telefones_formatados.append(f'81{telefone_formatado}')
            continue
        
        # Se não for possível formatar, mantém o original (ou pode retornar None)
        telefones_formatados.append(telefone) # (para manter o valor original)
    
    return Series(telefones_formatados, index=serie_telefone.index, name='TELEFONE_FORMATADO')