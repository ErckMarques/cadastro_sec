from dotenv import dotenv_values
from pathlib import Path

DADOS_ENTRADA = Path(__file__).parents[1].joinpath('dados_entrada',)
DADOS_SAIDA = DADOS_ENTRADA.parent.joinpath('dados_saida')
MESES = 'JANEIRO,FEVEREIRO,MARÇO,ABRIL,MAIO,JUNHO,JULHO,AGOSTO,SETEMBRO,OUTUBRO,NOVEMBRO,DEZEMBRO'.split(',')

# VARIAVEIS DO AMBIENTE CARREGADAS DO .env
DADOS_SITE = dotenv_values(Path().cwd().joinpath('.env'))

from cadastro._typings import CadastroProxy, Cadastro
from cadastro.extrair_dados import extrair_dados, extrair_dados_completos
from cadastro.extrair_dados_v2 import ExtratorDadosCadastro
from cadastro.cadastrar import Cadastrar