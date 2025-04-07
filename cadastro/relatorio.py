from cadastro.models import TemplateExportador
from pandas import ExcelWriter, DataFrame

from cadastro import DADOS_OUTPUT
from cadastro._log import log
from cadastro._typings import CadastroProxy, Cadastro

class Relatorio(TemplateExportador):
    """Classe responsável por gerar relatórios a partir de dados extraídos."""

    @staticmethod
    def gerar_relatorio(self) -> None:
        """Gera um relatório a partir dos dados extraídos."""
        dados: Cadastro = CadastroProxy.get_cadastro()
        try:
            with ExcelWriter(DADOS_OUTPUT, engine='openpyxl') as writer:
                if not dados['geral'].empty:
                    log.info('Registrando o Cadastros Geral')
                    # Exporta todos os dados extraidos
                    dados['geral'].to_excel(writer, sheet_name='Dados Gerais', index=False, startrow=2)

                if not dados['completos'].empty:
                    log.info('Registrando os Cadastros Completos')
                    # Exporta os dados completos
                    dados['completos'].to_excel(writer, sheet_name='Dados Completos', index=False, startrow=2)
                
                if not dados['faltantes'].empty:
                    log.info('Registrando os Cadastros Faltantes')
                    # Exporta os dados faltantes
                    dados['faltantes'].to_excel(writer, sheet_name='Dados Faltantes', index=False, startrow=2)
                
                if not dados['invalidados'].empty:
                    log.info('Registrando os Cadastros Inválidados')
                    # Exporta os dados inválidos
                    dados['invalidados'].to_excel(writer, sheet_name='Dados Inválidos', index=False, startrow=2)
                
                if not dados['nao_cadastrados']:
                    log.info('Registrando os Cadastros Não Registrados no Sistema da Secretaria')
                    # Exporta os dados não cadastrados
                    dados['nao_cadastrados'].to_excel(writer, sheet_name='Dados Cadastrados', index=False, startrow=2)
        except Exception as e:
            log.error('Erro ao gerar relatório', e)