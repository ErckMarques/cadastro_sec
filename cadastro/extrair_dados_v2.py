import logging

from pandas import concat, read_excel
from pandas import  DataFrame, ExcelWriter
from re import compile, Pattern

from cadastro import DADOS_EXCEL, DADOS_OUTPUT, MESES

class ExtratorDadosCadastro:
    """Esta classe é responsável por extrair os dados de cadastro de um arquivo excel e normalizá-los."""
    
    def __init__(self):
        self._cadastros: DataFrame | None = None
        self._cadastros_completos: DataFrame | None = None
        self._cadastros_faltantes: DataFrame | None = None
        self._cadastros_nao_validados: DataFrame | None = None
        self._header_sheets = ['NOME', 'APELIDO', 'ENDEREÇO', 'REFERENCIA', 'CPF', 'TELEFONE']
        
    @property
    def cadastros(self) -> DataFrame:
        return self._cadastros
    
    @property
    def cadastros_completos(self) -> DataFrame:
        return self._cadastros_completos
    
    def _normalizar_dados(self, dados: DataFrame) -> None:
        '''Esta função normaliza os dados de cadastro, deixando todo o texto em maiúsculo e removendo espaços em branco.'''
        for coluna in dados.columns:
            if dados[coluna].dtype == 'object':
                dados[coluna] = dados[coluna].str.upper().str.strip()        
    
    def extrair_dados(self) -> None:
        '''Esta função extrai os dados de cadastro de todos os meses e gera um DataFrame com todos os dados.'''

        if self._cadastros is not None:
            return

        aux = list()
        for mes in MESES:
            df = read_excel(DADOS_EXCEL, sheet_name=mes, header=6, usecols=self._header_sheets, names=self._header_sheets)
            aux.append(df)
    
        self._cadastros = concat(aux, ignore_index=True)
        self._normalizar_dados(self._cadastros)
    
    def extrair_dados_completos(self) -> None:
        '''Esta função extrai os dados de cadastro completos, ou seja, sem dados faltantes ou duplicados.'''

        if self._cadastros is None:
            self.extrair_dados()
        
        self._cadastros_completos = self._cadastros.dropna().drop_duplicates()
    
    def extrair_dados_faltantes(self) -> None:
        '''Esta função extrai os dados de cadastro que estão faltando, ou seja, com ao menos um dado faltante.'''
        if self._cadastros is None:
            self.extrair_dados()
        
        self._cadastros_faltantes = self._cadastros[self._cadastros[['REFERENCIA', 'CPF', 'TELEFONE']].isna().any(axis=1)]

    def extrair_e_classificar_dados(self) -> None:
        '''Esta função extrai os dados de cadastro, os dados completos e os dados faltantes.'''
        if None in (self._cadastros, self._cadastros_completos, self._cadastros_faltantes):
            self.extrair_dados()
            self.extrair_dados_completos()
            self.extrair_dados_faltantes()
            return
        logging.info('Os dados já foram extraídos e classificados.')

    def exportar_relatorio(self) -> None:
        '''Esta função exporta um relatorio com todos os dados, 
        os dados que tem ao menos um dado faltante e os dados que estão completos para um arquivo excel.
        '''

        if (self._cadastros is None or 
        self._cadastros_completos is None or 
        self._cadastros_faltantes is None):
            logging.error(
                'Alguns dados não foram extraídos e classificados. '
                'Por favor execute o método extrair_e_classificar_dados() antes de exportar o relatório.'
            )

        with ExcelWriter(DADOS_OUTPUT, engine='openpyxl') as writer:
            self._cadastros.to_excel(writer, sheet_name='CADASTRO GERAL', startrow=2, index=False)
            self._cadastros_completos.to_excel(writer, sheet_name='CADASTROS COMPLETOS', startrow=2, index=False)
            self._cadastros_faltantes.to_excel(writer, sheet_name='CADASTROS FALTANTES', startrow=2, index=False)

if __name__ == '__main__':
    extrator = ExtratorDadosCadastro()
    extrator.extrair_e_classificar_dados()
    extrator.exportar_relatorio()