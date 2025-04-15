from dotenv import dotenv_values
from pathlib import Path

DADOS_ENTRADA = Path(__file__).parents[1].joinpath('dados_entrada',)
DADOS_SAIDA = DADOS_ENTRADA.parent.joinpath('dados_saida')

# verifica e cria a pasta dos arquivos de saida, se ela não existir
if not DADOS_SAIDA.exists(): 
    DADOS_SAIDA.mkdir(parents=True, exist_ok=True)

# verifica se a pasta com os arquivos de entrada existe
if not DADOS_ENTRADA.exists() or not DADOS_ENTRADA.is_dir():
    raise FileNotFoundError('Diretório com os dados de entrada não existe')

for item in DADOS_ENTRADA.iterdir():
    if not item.is_dir() and not len(item.iterdir()):
        raise FileNotFoundError(f'Diretório "{item.stem}" não existem ou não contém os dados de entrada.')

MESES = 'JANEIRO,FEVEREIRO,MARÇO,ABRIL,MAIO,JUNHO,JULHO,AGOSTO,SETEMBRO,OUTUBRO,NOVEMBRO,DEZEMBRO'.split(',')

# VARIAVEIS DO AMBIENTE CARREGADAS DO .env
DADOS_SITE = dotenv_values(Path().cwd().joinpath('.env'))

from cadastro._typings import CadastroProxy, Cadastro
from cadastro.extrair_dados import extrair_dados, extrair_dados_completos
from cadastro.extrair_dados_v2 import ExtratorDadosCadastro
from cadastro.cadastrar import Cadastrar