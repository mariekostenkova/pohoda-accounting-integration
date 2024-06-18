import os

os.environ['INPUT_DIR'] = 'C:\\Users\\Administrator\Documents\\xml'
os.environ['OUTPUT_DIR'] = 'C:\\Users\\Administrator\\Documents\\xml\\Response'
INPUT_DIR = os.environ['INPUT_DIR']
OUTPUT_DIR = os.environ['OUTPUT_DIR']


POHODA_PATH = os.getenv('POHODA_PATH')
POHODA_INTEGRATION_BASE_URL = os.environ.get('POHODA_INTEGRATION_BASE_URL')
INI_FILE = os.getenv('INI_FILE')

USER_POHODA = os.getenv('USER_POHODA')
PASSWORD = os.getenv('PASSWORD')

AZURE_DEVOPS_PAT = os.getenv('AZURE_DEVOPS_PAT')
