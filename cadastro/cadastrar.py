from pandas import DataFrame

from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait

from cadastro import DADOS_SITE
from cadastro._log import log

class Cadastrar:
    def __init__(self, dados_cadastro: DataFrame):
        self._dados_cadastro = dados_cadastro
        self._driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self._wait = WebDriverWait(self._driver, 10)

    def logar(self):
        self._driver.get(DADOS_SITE.get('URL'))
        log.info('Acessando site do Sistema da Secretaria de Agricultura')
        log.info('Logando no sistema...Aguarde')
        field_user = self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, DADOS_SITE.get('FIELD_USER'))))
        field_pwd = self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, DADOS_SITE.get('FIELD_PWD'))))
        log.info('Preenchendo usuário e senha')
        field_user.send_keys(DADOS_SITE.get('USUARIO'))
        field_pwd.send_keys(DADOS_SITE.get('SENHA'))

        log.info('Logando no sistema')
        self._driver.find_element(By.TAG_NAME, 'button').click()
        if self._wait.until(EC.presence_of_element_located((By.CLASS_NAME, DADOS_SITE.get('GRAFICO')))):
            log.info('Logado com sucesso')
            return
        log.error('Erro ao logar no sistema. Encerrando driver...')
        self._driver.quit()


    def cadastrar(self):
        log.info('Abrindo página de cadastro')
        menu_cad = self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, DADOS_SITE.get('CAD'))))
        not_cadastrados = list()
        
        if self._wait.until(EC.presence_of_element_located((By.TAG_NAME, 'input'))):
            
            log.info('Identificando Campos do formulário de Cadastro')
            elementos = self._loc_campos()
            nome = elementos.get('name'); apelido = elementos.get('apelido'); cpf = elementos.get('cpf'); phone = elementos.get('phone')
            ref = elementos.get('referencia'); local = elementos.get('local'); btn_cad = elementos.get('btn')
            log.info('Preenchendo formulário com os dados de cadastro completo')
            for row in self._dados_cadastro.itertuples():
                log.info(f'Cadastrando {row.NOME}, {row.CPF}')
                nome.send_keys(row.NOME)
                apelido.send_keys(row.APELIDO)
                cpf.send_keys(row.CPF)
                phone.send_keys('81' + str(row.TELEFONE))
                ref.send_keys(row.REFERENCIA)
                local.select_by_value(row.ENDEREÇO)
                btn_cad.click()
                if nome.get_attribute('value') == '':
                    log.info(f'{row.NOME} cadastrado com sucesso')
                else:
                    log.error(f'Erro ao cadastrar {row.NOME}')

    def _loc_campos(self) -> dict[str, WebElement | Select]:
        """Localiza e retorna um dicionário de elementos web (input, select, button) com chaves específicas."""
        web_elements = {}
        log.info('Capturando referencia dos elementos da ficha cadastral')
        # Captura inputs cujo atributo 'name' está em DADOS_SITE
        for element in self._wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'input'))):
            if (name := element.get_attribute('name')) in DADOS_SITE.values():
                log.info(f'Pegando referencia do elemento: {name}')
                web_elements[name] = element
        
        # adiciona o elemento 'outros'
        log.info('Pegando referencia de Outros e Localidade.')
        web_elements['outros'] = self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, DADOS_SITE.get('CLASS'))))
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