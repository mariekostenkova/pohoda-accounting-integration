import os

LOGGER_NAME = os.getenv('LOGGER_NAME', 'integration-pohoda-logger')

# Informaton about INI file
INI_FILE = os.getenv('INI_FILE')
INPUT_DIR = os.environ['INPUT_DIR']
OUTPUT_DIR = os.environ['OUTPUT_DIR']

# Pohoda executable information
POHODA_EXECUTABLE_PATH = os.environ['POHODA_EXECUTABLE_PATH']
POHODA_USER = os.environ['POHODA_USER']
POHODA_PASSWORD = os.environ['POHODA_PASSWORD']
# POHODA_INTEGRATION_BASE_URL = os.environ.get('POHODA_INTEGRATION_BASE_URL')

