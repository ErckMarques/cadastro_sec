from dotenv import dotenv_values
from pathlib import Path

DADOS_EXCEL = Path(__file__).parents[1].joinpath('dados', 'abastecimento_2024.xlsx')
DADOS_OUTPUT = DADOS_EXCEL.parent.joinpath('cadastros.xlsx')
MESES = 'JANEIRO,FEVEREIRO,MARÇO,ABRIL,MAIO,JUNHO,JULHO,AGOSTO,SETEMBRO,OUTUBRO,NOVEMBRO,DEZEMBRO'.split(',')

DADOS_SITE = dotenv_values(Path().cwd().joinpath('.env'))

from cadastro.extrair_dados import extrair_dados, extrair_dados_completos
from cadastro.extrair_dados_v2 import ExtratorDadosCadastro
from cadastro.cadastrar import Cadastrar
from cadastro.normalizar_planilha import NormalizarXl
from cadastro._log import log