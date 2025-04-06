from pandas import concat, read_excel
from pandas import  DataFrame, ExcelWriter

from cadastro._log import log
from cadastro._typings import CadastroProxy, Cadastro
from cadastro import DADOS_EXCEL, DADOS_OUTPUT, MESES
from cadastro.normalizar_dados import NormalizarDadosCadastro

class ExtratorDadosCadastro:
    """Esta classe é responsável por extrair os dados de cadastro de um arquivo excel."""
    
    def __init__(self):
        self._cadastros: Cadastro = CadastroProxy.get_cadastro()
        self._normal: NormalizarDadosCadastro | None = None
        self._header_sheets = ['NOME', 'APELIDO', 'ENDEREÇO', 'REFERENCIA', 'CPF', 'TELEFONE']
    
    def _normalizar_dados(self) -> None:
        '''Esta função normaliza os dados de cadastro com a classe NormalizarDadosCadastro.
        A normalização é feita da seguinte forma:
            1. resolvendo apelidos faltantes
            2. verificando o formato dos cpf's (ainda não os valida)
            3. normalizando o endereço extraindo o texto entre () com aplicação vetorial de regex
            4. normalizando a referencia do endereço
            5. normalizando o telefone (ainda não os valida)
            6. deixa todo o texto em uppercase
        '''
        if self._normal is None:
            self._normal = NormalizarDadosCadastro(self._cadastros['geral'])
            
        self._cadastros = self._normal.normalizar() # Normaliza os dados de cadastro. Retorna as chaves 'geral' e 'invalidados'.

    def _extrair_dados(self) -> None:
        '''Esta função extrai os dados de cadastro de todos os meses e gera um DataFrame com todos os dados. 
        Remove dados duplicados e normaliza os dados.
        '''
        
        # verifica se os dados já foram extraídos, se sim, retorna os dados já extraídos
        if not self._cadastros.get('geral').empty:
            log.info('Os dados já foram extraídos. Acesse-os chamando CadastroProxy.get_cadastro(). Retornando...')
            return

        # inicia o processo de extração dos dados
        log.info('Iniciando a extração dos dados.')
        aux = list()
        for mes in MESES:
            log.info(f'Extraindo dados do mês de {mes}')
            # lê os dados do mês e adiciona ao DataFrame auxiliar
            df = read_excel(DADOS_EXCEL, sheet_name=mes, header=6, usecols=self._header_sheets, names=self._header_sheets)
            aux.append(df)
    
        # concatena os dados de todos os meses e remove duplicados
        self._cadastros['geral'] = concat(aux, ignore_index=True).drop_duplicates()
        log.info('Dados extraídos com sucesso!')

    def _extrair_dados_completos(self) -> None:
        '''Esta função extrai os dados de cadastro completos, ou seja, sem dados faltantes.'''

        if not self._cadastros.get('geral').empty:
            log.info('Os dados já foram extraídos. Acesse-os chamando CadastroProxy.get_cadastro(). Retornando...')
            self._extrair_dados()
        
        if not self._cadastros.get('completos').empty:
            log.info("Os dados completos já foram extraídos. Acesse-os chamando CadastroProxy.get_cadastro()['completos']. Retornando...")
            return

        log.info('Extraindo dados completos...')
        self._cadastros['completos'] = self._cadastros.get('geral').dropna()
    
    def _extrair_dados_faltantes(self) -> None:
        '''Esta função extrai os dados de cadastro que estão faltando, ou seja, com ao menos um dado faltante.'''
        
        if not self._cadastros.get('geral').empty:
            log.info('Os dados já foram extraídos. Acesse-os chamando CadastroProxy.get_cadastro(). Retornando...')
            self._extrair_dados()
        
        if not self._cadastros.get('faltantes').empty:
            log.info("Os dados faltantes já foram extraídos. Acesse-os chamando CadastroProxy.get_cadastro()['faltantes']. Retornando...")
            return

        log.info('Extraindo dados faltantes...')
        self._cadastros['faltantes'] = self._cadastros['geral'][self._cadastros['geral'][['REFERENCIA', 'CPF', 'TELEFONE']].isna().any(axis=1)]

    def extrair_e_classificar_dados(self) -> None:
        '''Esta função extrai os dados de cadastro, os dados completos e os dados faltantes.
        Ela também aplica os métodos de normalização aos dados. Também atualiza o dicionário central com os dados extraídos.
        '''
        try:  
            if (self._cadastros.get('geral').empty and self._cadastros.get('completos').empty and self._cadastros.get('faltantes').empty):
                self._extrair_dados()
                self._normalizar_dados()
                self._extrair_dados_completos()
                self._extrair_dados_faltantes()
                log.info('Os dados já foram extraídos e classificados!')
                
                log.info('Atualizando o dicionário central...')
                for key, value in self._cadastros.items():
                    CadastroProxy.update_cadastro(key, value, self)
                
                return
            log.info('Retornando Dados... Acesse-os chamando CadastroProxy.get_cadastro()')
        except Exception as e:
            log.error('Ocorreu um erro ao tentar extrair os dados.', e)