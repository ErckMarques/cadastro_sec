'''Este módulo contém a definição do dicionário central e o proxy para acesso controlado.'''

from typing import TypedDict, Any
from pandas import DataFrame
from copy import deepcopy

class Cadastro(TypedDict):
    """Estrutura tipada do dicionário central."""
    geral: DataFrame             # DataFrame com todos os dados extraídos
    completos: DataFrame         # DataFrame com dados completos (sem faltas ou duplicados)
    faltantes: DataFrame         # DataFrame com dados faltantes (com ao menos um dado faltante)
    invalidados: DataFrame       # DataFrame com dados invalidados (com erros de validação)
    cadastrados: DataFrame       # DataFrame com dados cadastrados (completo e sem faltas)
    nao_cadastrados: DataFrame   # DataFrame com dados não cadastrados (completo e sem faltas)

class CadastroProxy:
    """Proxy que controla o acesso ao dicionário central."""
    _instance: 'CadastroProxy' = None
    _cadastro_central: Cadastro = {
        "geral": DataFrame(),
        "completos": DataFrame(),
        "faltantes": DataFrame(),
        "nao_validados": DataFrame(),
        "cadastrados": DataFrame(),
        "nao_cadastrados": DataFrame(),
    }
    # Nome da classe autorizada a modificar o cadastro (evita importar a classe)
    _allowed_writer: str = "ExtratorDadosCadastro"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_cadastro(cls) -> Cadastro:
        """Retorna uma cópia segura do dicionário central."""
        return deepcopy(cls._cadastro_central)

    @classmethod
    def update_cadastro(cls, key: str, value: DataFrame, caller: Any) -> None:
        """Atualiza o dicionário central (apenas para a classe autorizada)."""
        caller_class_name = caller.__class__.__name__
        if caller_class_name != cls._allowed_writer:
            raise PermissionError(
                f"Apenas {cls._allowed_writer} pode modificar o cadastro central. "
                f"Classe chamadora: {caller_class_name}"
            )
        cls._cadastro_central[key] = value.copy()