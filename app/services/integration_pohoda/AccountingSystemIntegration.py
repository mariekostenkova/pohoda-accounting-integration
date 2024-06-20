import logging
import os
import subprocess
import time
from enum import Enum
from CanonicalDataModels import ExpenseDocumentData
from defusedxml.ElementTree import fromstring as ET

from app.config import LOGGER_NAME
import asyncio
logger = logging.getLogger(LOGGER_NAME)


class FileStatus(Enum):
    OK = 'OK'
    NOT_CHANGED = 'NOT_CHANGED'
    ERROR = 'ERROR'

class AccountingSystemIntegrationError(Exception):
    """ This exception.... """

class PollingError(AccountingSystemIntegrationError):
    """ This exception.... """


def json_to_xml(json_obj, line_padding=''):
    """Converts a dictionary to an XML."""
    result_list = []
    if isinstance(json_obj, dict):
        for tag_name, sub_obj in json_obj.items():
            result_list.append(f'{line_padding}<{tag_name}>')
            result_list.append(json_to_xml(sub_obj, '\t' + line_padding))
            result_list.append(f'{line_padding}</{tag_name}>')
    elif isinstance(json_obj, list):
        for sub_elem in json_obj:
            result_list.append(json_to_xml(sub_elem, line_padding))
    else:
        result_list.append(f'{line_padding}{json_obj}')
    return '\n'.join(result_list)


class AccountingSystemIntegration:
    def __init__(self, pohoda_path: str, user: str, password: str, ini_file: str):
        self.pohoda_path = pohoda_path
        self.user = user
        self.password = password
        self.ini_file = ini_file

    async def execute_pohoda_command(self, input_file: str):
        """Executes command in POHODA"""
        try:
            result = subprocess.call([self.pohoda_path, '/XML', self.user, self.password, self.ini_file])
            if result != 0:
                raise AccountingSystemIntegrationError(f'Pohoda command execution failed with return code {result}')
        except Exception as e:
            raise AccountingSystemIntegrationError(f'Command execution failed: {e}')

    async def process_xml_file(self, filename: str, input_dir: str):
        """Processes all XML files in the directory by executing the POHODA command on each file."""
        try:
            input_file = os.path.join(input_dir, filename)
            logger.info(f'Processing file: {input_file}')
            await self.execute_pohoda_command(input_file)
        except Exception as e:
            logger.debug(f'Error processing XML files: {e}')
            raise AccountingSystemIntegrationError(f'Error processing XML files: {e}')

    @staticmethod
    async def check_file_status(folder_path, filename):
        """ Checks if the file exists in the folder """
        try:
            if filename in os.listdir(folder_path):
                return FileStatus.OK
            else:
                return FileStatus.NOT_CHANGED
        except Exception as e:
            logger.debug(f'Error during file check: {e}')
            return FileStatus.ERROR

    async def poll_folder(self, folder_path, filename, interval, max_retries=10):
        """Add status """
        retries = 0
        while retries < max_retries:
            status = await self.check_file_status(folder_path, filename)
            if status == FileStatus.OK:
                logger.info(f"File '{filename}' found in folder '{folder_path}'.")
                break
            elif status == FileStatus.NOT_CHANGED:
                logger.info(f"File '{filename}' not found. Checking again in {interval} seconds.")
            elif status == FileStatus.ERROR:
                logger.info('An error occurred. Retrying in a moment.')
            retries += 1
            await asyncio.sleep(interval)
        else:
            logger.warning(f"File '{filename}' not found after {max_retries} retries.")
            raise AccountingSystemIntegrationError(f"File '{filename}' not found after {max_retries} retries.")

    @staticmethod
    async def parse_pohoda_xml(file_path: str) -> str:
        """Parses a Pohoda XML file to extract external_id."""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            for elem in root.iter('ExternalIdTag'):
                external_id = elem.text
                break
            else:
                external_id = None
            if external_id:
                logger.info(f'External ID: {external_id}')
            else:
                logger.info('External ID not found in the XML.')
            return external_id
        except ET.ParseError as e:
            raise AccountingSystemIntegrationError(f'Error parsing the XML file: {e}')
        except FileNotFoundError:
            raise AccountingSystemIntegrationError('The file was not found.')
