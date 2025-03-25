'''
Este módulo contém a classe NormalizarXl,
que é responsável por normalizar os dados de um arquivo excel com formato já definido.
'''

from pandas import DataFrame, read_excel, concat
from pandas import ExcelWriter

class NormalizarXl:
    
    def __init__(self):
        self._column_names = ['NOME ', 'APELIDO ', 'ENDEREÇO', 'CPF', 'TELEFONE']
