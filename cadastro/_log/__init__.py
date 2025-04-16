import logging as log

from cadastro import ENV_VARS

if ENV_VARS.get('MODE') == 'dev':
    log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

log.basicConfig(level=log.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
