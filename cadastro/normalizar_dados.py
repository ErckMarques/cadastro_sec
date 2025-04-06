'''
Este módulo contém a classe NormalizarXl,
que é responsável por normalizar os dados de um arquivo excel com formato já definido.
'''
from re import IGNORECASE

from pandas import DataFrame, concat

from cadastro._log import log
from cadastro._typings import Cadastro
from cadastro.errors import (NormalizarApelidoError, 
        NormalizarEnderecoError, 
        NormalizarReferenciaError,
        NormalizarCpfError, 
        NormalizarTelefoneError
)
from cadastro.models import TemplateExportador

def _normalizar_referencia(dados: DataFrame) -> DataFrame:
    pass

class NormalizarDadosCadastro(TemplateExportador):
    
    def __init__(self, dados: DataFrame) -> None:
        self._dados: DataFrame = dados
        self._column_names = ['NOME', 'APELIDO', 'ENDEREÇO', 'CPF', 'TELEFONE']
        self._normalizados: DataFrame = DataFrame() # DataFrame com os dados normalizados, sobrescreve 'geral'
        self._invalidos: DataFrame = DataFrame()    # DataFrame com os dados inválidos, sobrescreve 'invalidados'
    
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
            # Verifica se o apelido é nulo e substitui pelo primeiro nome
            self._dados['APELIDO'] = self._dados['APELIDO'].str.fillna(self._dados['NOMES'].str.split().str[0])
            # aplica upper_case e remove espaços em branco
            self._dados['APELIDO'] = self._dados['APELIDO'].str.upper().str.strip()
        except Exception as e:
            raise NormalizarApelidoError(f"Erro ao normalizar apelido: {e}")
        
    def _normalizar_endereco(self):
        '''Função para normalizar o endereço, corrigindo alguns nomes e localidades. extrair o texto '()' com regex.'''
        try:
            self._dados['ENDEREÇO'] = self._dados['ENDEREÇO'].str.extract(r'^S(I|Í|IT)[TIO]*\s+(.+)$', flags=IGNORECASE)[1]
            self._dados['ENDEREÇO'].str.upper().str.strip()
        except Exception as e:
            raise NormalizarEnderecoError(f"Erro ao normalizar endereço: {e}")

    def _normalizar_referencia(self):
        '''Esta função normaliza as referencias dos dados de cadastro.'''
        try:
            # Verifica se a coluna 'REFERENCIA' não existe
            if self._dados.get('REFERENCIA') is None:
                # Cria a coluna 'REFERENCIA' e extrai o texto entre parênteses da coluna 'ENDEREÇO'
                self._dados['REFERENCIA'] = self._dados['ENDEREÇO'].str.extract(r'\((.*?)\)', flags=IGNORECASE)[0]
                # Linhas com valores nulos ou NaN são preenchidas com 'SEM REFERENCIA'
                self._dados['REFERENCIA'].fillna('SEM REFERENCIA', inplace=True)
                self._dados['REFERENCIA'].str.upper().str.strip()
            else:
                # Se a coluna 'REFERENCIA' já existe, 
                self._dados['REFERENCIA'] = self._dados['ENDEREÇO'].str.extract(r'\((.*?)\)', flags=IGNORECASE)[0]
                # apenas extrai o texto entre parênteses, se houver.
                self._dados['REFERENCIA'] = self._dados['REFERENCIA'].str.replace(r'[()]', '', regex=True)
                self._dados['REFERENCIA'].str.upper().str.strip()
        except Exception as e:
            raise NormalizarReferenciaError(f"Erro ao normalizar referência: {e}")
    
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
            r'819\1-\2', 
            regex=True
        )
        
        # Atualiza DataFrame
        self._dados.loc[mask_validos, 'TELEFONE'] = telefones_validos
        self._invalidos = self._dados[~mask_validos].copy()
        self._dados = self._dados[mask_validos].copy()
    
    def normalizar(self) -> Cadastro:
        '''Aplica todas as normalizaçãoes para o conjunto de dados e os retorna(?)'''
        try:
            self._normalizar_apelido()
            self._normalizar_referencia()
            self._normalizar_endereco()
            self._normalizar_cpf()
            self._normalizar_telefone()
        except NormalizarApelidoError as e:
            log.error(f"Erro ao normalizar apelido: {e}")
        except NormalizarEnderecoError as e:
            log.error(f"Erro ao normalizar endereço: {e}")
        return self.dados_normalizados