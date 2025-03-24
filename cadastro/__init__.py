from pathlib import Path

from extrair_dados import extrair_dados, extrair_dados_completos

DADOS_EXCEL = Path(__file__).parents[1].joinpath('dados', 'abastecimento_2024.xlsx')
DADOS_OUTPUT = DADOS_EXCEL.parent.joinpath('cadastros.xlsx')
MESES = 'JANEIRO,FEVEREIRO,MARÇO,ABRIL,MAIO,JUNHO,JULHO,AGOSTO,SETEMBRO,OUTUBRO,NOVEMBRO,DEZEMBRO'.split(',')