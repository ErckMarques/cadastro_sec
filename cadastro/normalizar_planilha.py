'''
Este módulo contém a classe NormalizarXl,
que é responsável por normalizar os dados de um arquivo excel com formato já definido.
'''

from pandas import DataFrame, concat
from pandas import ExcelWriter, Series
from re import compile, match ,Pattern

from cadastro import log

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
    
    def _normalizar_apelido(self):
        '''Função para 'normalizar' o apelido, quando este não existir utilizar o primeiro nome da pessoa'''
        try:
            self._dados['APELIDO'] = self._dados['APELIDO'].str.fillna(self._dados['NOMES'].str.split().str[0])
        except Exception as e:
            log.error('Ocorreu um erro normalizar a coluna de apelidos', e)

    def _normalizar_endereco():
        '''Função para normalizar o endereço, corrigindo alguns nomes e localidades. extrair o texto '()' com regex.'''
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

    def _normalizar_telefone(self) -> None:
        '''Formata telefones válidos (9XXXX-XXXX) e separa inválidos.'''
        telefones = self._dados['TELEFONE'].astype(str).str.replace(r'[^\d]', '', regex=True)
        
        # Identifica telefones válidos (9 dígitos, começando com 9)
        mask_validos = telefones.str.match(r'^9?\d{8}$')  # Aceita 8 ou 9 dígitos
        
        # Formata os válidos: 81 + 9XXXX-XXXX
        telefones_validos = telefones[mask_validos].str.replace(
            r'^9?(\d{4})(\d{4})$', 
            r'9\1-\2', 
            regex=True
        )
        
        # Atualiza DataFrame
        self._dados.loc[mask_validos, 'TELEFONE'] = telefones_validos
        self._invalidos = self._dados[~mask_validos].copy()
        self._dados = self._dados[mask_validos].copy()
    
    def normalizar(self) -> DataFrame:
        '''Aplica todas as normalizaçãoes para o conjunto de dados e os retorna(?)'''
        if self._normalizados is None:
            self._normalizar_apelido()
            self._normalizar_endereco()
            self._normalizar_referencia()
            self._normalizar_cpf()
            self._normalizar_telefone()

        return self.dados_normalizados