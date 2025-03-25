import pytest

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from cadastro import Cadastrar

@pytest.fixture(scope='module')
def drive():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    yield driver
    driver.quit()

