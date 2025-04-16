from time import sleep
from pandas import DataFrame

from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidElementStateException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait

from cadastro import ENV_VARS
from cadastro._log import log

class Login:
    """Classe para realizar o login no sistema. Pega os dados do site e do usuário do ambiente(envvars)."""
    def __init__(self, driver: webdriver.Chrome):
        self._driver = driver
        self._wait = WebDriverWait(self._driver, 10)
    
    def logar(self):
        try:
            log.info('Acessando site do Sistema da Secretaria de Agricultura')
            self._driver.get(ENV_VARS.get('URL'))
            log.info('Logando no sistema...Aguarde')
            field_user = self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ENV_VARS.get('FIELD_USER'))))
            field_pwd = self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ENV_VARS.get('FIELD_PWD'))))
            log.info('Preenchendo usuário e senha')
            field_user.send_keys(ENV_VARS.get('USUARIO'))
            field_pwd.send_keys(ENV_VARS.get('SENHA'))

            log.info('Logando no sistema')
            self._driver.find_element(By.TAG_NAME, 'button').click()
            if self._wait.until(EC.presence_of_element_located((By.CLASS_NAME, ENV_VARS.get('GRAFICO')))):
                log.info('Logado com sucesso')
                return
            log.error('Erro ao logar no sistema. Encerrando driver...')
            self._driver.quit()
        except Exception as e:
            log.error('Um erro ocorreu ao logar no sistema:', e.args(-1))
            self._driver.quit()
        

class Cadastrar:
    def __init__(self, driver: webdriver.Chrome, dados_cadastro: DataFrame):
        self._dados_cadastro = dados_cadastro
        self._driver = driver
        self._wait = WebDriverWait(self._driver, 10)

    def cadastrar(self):
        log.info('Abrindo página de cadastro')
        menu_cad = self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ENV_VARS.get('CAD'))))
        not_cadastrados = list()
        
        if self._wait.until(EC.presence_of_element_located((By.TAG_NAME, 'input'))):
            
            log.info('Identificando Campos do formulário de Cadastro')
            elementos = self._loc_campos()
            nome = elementos.get('name'); apelido = elementos.get('apelido'); cpf = elementos.get('cpf'); phone = elementos.get('phone')
            ref = elementos.get('referencia'); local = elementos.get('local'); btn_cad = elementos.get('btn')
            log.info('Preenchendo formulário com os dados de cadastro completo')
            try:
                for row in self._dados_cadastro.itertuples():
                    log.info(f'Cadastrando {row.NOME}, {row.CPF}')
                    sleep(0.3)
                    nome.clear()
                    nome.send_keys(row.NOME)
                    sleep(0.3)
                    apelido.clear()
                    apelido.send_keys(row.APELIDO)
                    sleep(0.3)
                    cpf.click()
                    cpf.clear()
                    cpf.send_keys(row.CPF)
                    sleep(0.3)
                    phone.click()
                    phone.clear()
                    phone.send_keys('81' + str(row.TELEFONE))
                    sleep(0.2)
                    ref.send_keys(row.REFERENCIA)
                    sleep(0.1)
                    local.select_by_value(row.ENDEREÇO)
                    sleep(0.2)
                    btn_cad.click()
                    if nome.get_attribute('value') == '':
                        log.info(f'{row.NOME} cadastrado com sucesso')
                    else:
                        log.error(f'Erro ao cadastrar {row.NOME}')
                        not_cadastrados.append(row)
            except InvalidElementStateException as e:
                log.error('Erro ao acessar um dos elementos da ficha cadastral', e)
                not_cadastrados.append(row)
            except Exception as e:
                log.error(f'Aconteceu um erro ao cadastrar os dados de {row.NOME}: {row.CPF}')
                not_cadastrados.append(row)

    def _loc_campos(self) -> dict[str, WebElement | Select]:
        """Localiza e retorna um dicionário de elementos web (input, select, button) com chaves específicas."""
        web_elements = {}
        log.info('Capturando referencia dos elementos da ficha cadastral')
        # Captura inputs cujo atributo 'name' está em ENV_VARS
        for element in self._wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'input'))):
            if (name := element.get_attribute('name')) in ENV_VARS.values():
                log.info(f'Pegando referencia do elemento: {name}')
                web_elements[name] = element
        
        # adiciona o elemento 'outros'
        log.info('Pegando referencia de Outros e Localidade.')
        web_elements['outros'] = self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ENV_VARS.get('CLASS'))))
        # Adiciona o elemento 'select' com a chave 'local'
        web_elements['local'] = Select(self._wait.until(EC.presence_of_element_located((By.TAG_NAME, 'select'))))

        # Adiciona o último botão encontrado com a chave 'botao'
        botoes = self._driver.find_elements(By.TAG_NAME, 'button')
        for btn in botoes:
            if btn.text == 'Avançar':
                web_elements['btn'] = btn
        
        return web_elements
        
    def fechar(self):
        self._driver.quit()

class AlterarGenero:

    def __init__(self, driver: webdriver.Chrome, dados_cadastro: DataFrame):
        self._driver = driver
        self._dados_cadastro = dados_cadastro
        self._wait = WebDriverWait(self._driver, 10)
    
    def _abrir_todos_cadastros(self) -> None | WebElement:
        """Acessa a página de todos os dados cadastrados no sistema."""
        try:
            log.info('Acessando página de SELEÇÃO de cadastro')
            # Acessa o menu dos cadastros
            self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ENV_VARS.get('GERAL')))).click()
            log.info('Aguarde...')
            if cpf:=self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ENV_VARS.get('SRC_CPF')))):
                log.info('Paginas de cadastro carregada com sucesso')
                return cpf
            log.error('Não foi possível acessar a página de cadastro')
            return None
        except NoSuchElementException as e:
            log.error('Erro ao acessar a página de cadastro', e)
            self._driver.quit()
            return None
        except Exception as e:
            log.error('Erro ao acessar a página de cadastro', e)
            self._driver.quit()
            return None
        
    def _abrir_cadastro(self, cpf: str) -> None | WebElement:
        """Acessa o cadastro do usuário."""
        try:
            log.info(f'Acessando cadastro de CPF: {cpf}')
            if self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ENV_VARS.get('SRC_CPF')))):
                log.info('Página de cadastro carregada com sucesso')
                log.info(f'Acessando cadastro de {cpf}')
                self._driver.find_element(By.CSS_SELECTOR, ENV_VARS.get('SRC_CPF')).send_keys(cpf + Keys.ENTER)
                return self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ENV_VARS.get('CADASTRO'))))
            log.error('Não foi possível acessar a página de cadastro')
            return None
        except NoSuchElementException as e:
            log.error('Erro ao acessar a página de cadastro', e)
            self._driver.quit()
            return None
    
    def _alterar_genero(self, genero: str) -> None | WebElement:
        """Altera o gênero do cadastro."""
        try:
            log.info('Alterando gênero do cadastro')
            if self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ENV_VARS.get('GENERO')))):
                log.info('Página de cadastro carregada com sucesso')
                select = Select(self._driver.find_element(By.CSS_SELECTOR, ENV_VARS.get('GENERO')))
                select.select_by_value(genero)
                return self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ENV_VARS.get('SALVAR'))))
            log.error('Não foi possível acessar a página de cadastro')
            return None
        except NoSuchElementException as e:
            log.error('Erro ao acessar a página de cadastro', e)
            self._driver.quit()
            return None
    
    def _salvar_alteracao(self):
        """Salva as alterações feitas no cadastro."""
        pass

    def _voltar_a_pagina_todos_cadastros(self):
        pass

    def alterar(self, cpf: str, genero: str) -> None:
        """Altera o gênero do cadastro."""
        log.info('Aguarde...')
        if self._abrir_todos_cadastros():
            if self._abrir_cadastro(cpf):
                if self._alterar_genero(genero):
                    log.info(f'Gênero alterado para {genero}')
                    if self._salvar_alteracao():
                        log.info('Alteração salva com sucesso')
                        return
                    log.error('Erro ao salvar alteração')
                    return
                log.error('Erro ao alterar gênero')
                return
            log.error('Erro ao acessar cadastro')
            return
        log.error('Erro ao acessar página de cadastro')
        # aplicar early return para evitar o uso de else e tantas identações