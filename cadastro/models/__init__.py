'''Este módulo define a interface para extratores e exportadores de dados de arquivos excel(utilizando template method).'''
from abc import ABC, abstractmethod

class TemplateExtrator(ABC):
    '''Classe abstrata para extratores de dados de arquivos excel.'''

    @abstractmethod
    def extrair_e_classificar_dados(self) -> dict:
        '''Esta função extrai os dados de cadastro, os dados completos e os dados faltantes.'''
        raise NotImplementedError("Método não implementado.")

class TemplateExportador(ABC):
    '''Classe abstrata para exportadores de dados para arquivos excel.'''
    
    @abstractmethod
    def exportar_relatorio(self) -> None:
        '''Esta função exporta um relatorio com todos os dados, cadastro completo e cadastro faltante para um arquivo excel.'''
        raise NotImplementedError("Método não implementado.")