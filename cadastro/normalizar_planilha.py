'''
Este módulo contém a classe NormalizarXl,
que é responsável por normalizar os dados de um arquivo excel com formato já definido.
'''

from pandas import DataFrame, concat
from pandas import ExcelWriter, Series
from re import compile, match ,Pattern

class NormalizarXl:
    
    def __init__(self, dados: DataFrame):
        self._dados = dados
        self._column_names = ['NOME', 'APELIDO', 'ENDEREÇO', 'CPF', 'TELEFONE']
        self._normalizados: DataFrame = DataFrame(None)
        self._invalidos: DataFrame = DataFrame(None)
    
    @property
    def dados_normalizados(self) -> DataFrame:
        '''Retorna os dados normalizados'''
        return self._normalizados
    
    @property
    def dados_invalidos(self) -> DataFrame:
        '''Retorna os dados inválidos'''
        return self._invalidos
    
    def _normalizar_apelido():
        '''Função para 'normalizar' o apelido, quando este não existir utilizar o primeiro nome da pessoa'''
        pass

    def _normalizar_endereco():
        '''Função para normalizar o endereço, corrigindo alguns nomes e localidades.'''
        pass

    def _normalizar_referencia(self):
        '''Esta função normaliza as referencias dos dados de cadastro.'''
        self._dados['ENDEREÇO'] = self._dados['ENDEREÇO'].str.upper().str.strip().str.replace(')', '').str.upper()
    
    def _normalizar_cpf(self) -> None:
        '''Esta função normaliza o CPF dos dados de cadastro.'''
        
        # Remove caracteres que não sejam dígitos e os substitui por ''
        cpfs = self._dados['CPF'].astype(str).str.replace(r'[^\d]', '', regex=True).str.strip()
        # mascara para cpfs com 11 digitos
        mask_validos = cpfs.str.len() == 11

        # Separa válidos/inválidos
        self._invalidos = concat(self._invalidos, self._dados[~mask_validos].copy(), ignore_index=True)
        self._dados = self._dados[mask_validos].copy()

    def _normalizar_telefone(self):

        # remove caracteres que não sejam dígitos e espaços em branco
        self._dados['TELEFONE'] = self._dados['TELEFONE'].astype(str).str.replace(r'[^\d]', '', regex=True).str.strip()
    
    def normalizar(self) -> DataFrame:
        '''Aplica todas as normalizaçãoes para o conjunto de dados e os retorna(?)'''
        if self._normalizados is None:
            self._normalizar_apelido()
            self._normalizar_endereco()
            self._normalizar_referencia()
            self._normalizar_cpf()
            self._normalizar_telefone()

        return self.dados_normalizados