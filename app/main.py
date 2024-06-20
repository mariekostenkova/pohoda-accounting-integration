import base64
# import multiprocessing
import os
import uvicorn
from CanonicalDataModels import ExpenseDocument
from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import http_exception_handler
from GrantonLogTrace import setup_logging
from PartyIdentity import PartyIdentity

from app.config import (INI_FILE, INPUT_DIR, LOGGER_NAME, OUTPUT_DIR,
                        POHODA_EXECUTABLE_PATH, POHODA_PASSWORD, POHODA_USER)
from app.models import Attachment
from app.services.integration_pohoda.AccountingSystemIntegration import (
    AccountingSystemIntegration, AccountingSystemIntegrationError, json_to_xml)

logger = setup_logging(logger_name=LOGGER_NAME)
logger.info('Pohoda Accounting System Integration is starting up.')
# workers = multiprocessing.cpu_count() * 2
# logger.debug(f'Number of workers: {workers}')


app = FastAPI(title='Pohoda Accounting System Integration')

@app.exception_handler(HTTPException)
async def http_exception_handler_logger(request, exc):
    logger.error(f'HTTPException: {exc.status_code} {exc.detail}')
    return await http_exception_handler(request, exc)



async def extract_party_identity(request: Request):
    """Extracts and constructs a PartyIdentity object from the JSON body of an incoming request."""
    try:
        body = await request.json()
        party_identity_data = body.get('party_identity')
        if not party_identity_data:
            raise ValueError("Missing 'party_identity' in request body")
        return PartyIdentity(**party_identity_data)
    except Exception as e:
        logger.error(f'Failed to extract PartyIdentity: {str(e)}')
        raise HTTPException(status_code=400, detail='Invalid party identity data')


async def extract_expense_document(request: Request):
    """Extracts an expense document from a JSON request."""
    try:
        body = await request.json()
        expense_document_data = body.get('expense_document')
        if not expense_document_data:
            raise ValueError("Missing 'expense_document' in request body")
        return ExpenseDocument(**expense_document_data)
    except Exception as e:
        logger.error(f'Failed to extract ExpenseDocument: {str(e)}')
        raise HTTPException(status_code=400, detail='Invalid expense document data')


async def create_dict(**kwargs) -> dict:
    """ Creates a dictionary with non-empty values only. """
    return {k: v for k, v in kwargs.items() if v is not None}

@app.post('/upload-expense-data')
async def upload_data(request: Request):
    """Endpoint to upload expense data."""
    try:
        party_identity = await extract_party_identity(request)
        expense_document = await extract_expense_document(request)
        record_id = expense_document.record_id
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f'Failed to upload expense data: {str(e)}')
        raise HTTPException(status_code=500, detail='Failed to upload expense data')
    else:
        logger.debug(f'New request received.', extra={'record_id': record_id, 'request_data': request.json()})

    try:
        json_data = {
            'party_identity': party_identity.dict(),
            'expense_document': expense_document.to_dict()
        }
        if json_data['expense_document']['payment']['payment_method'] == 'CARD':
            document_attributes = create_dict(
                party_business_id=json_data["party_identity"]["party_business_id"],
                party_db_name=json_data['party_identity']['party_db_name'],
                record_id=json_data["expense_document"]["record_id"],
                expense_type=json_data["expense_document"]["expense_document"]["expense_type"],
                total_amount=json_data["expense_document"]["expense_document"]["payment"]["total_amount"],
                payment_currency=json_data["expense_document"]["expense_document"]["payment"]["currency"]['code'],
                supplier_name=json_data["expense_document"]["expense_document"]["supplier"]["name"],
                supplier_company_id=json_data["expense_document"]["expense_document"]["supplier"]["company_id"],)

        xml_data = json_to_xml(json_data)
        result_filename = f'{record_id}.xml'
        with open(os.path.join(INPUT_DIR, result_filename), 'w') as file:
            file.write(xml_data)
    except:
        raise HTTPException(status_code=500, detail='Failed to convert ExpenseDocument to JSON')
    accounting_integration = AccountingSystemIntegration(POHODA_EXECUTABLE_PATH,
                                                         POHODA_USER,
                                                         POHODA_PASSWORD,
                                                         INI_FILE)
    try:
        await accounting_integration.process_xml_file(result_filename, INPUT_DIR)
    except AccountingSystemIntegrationError as acc_e:
        logger.error(f'Error processing XML files: {acc_e}')
        raise HTTPException(status_code=500, detail='Error processing XML files')

    await accounting_integration.poll_folder(OUTPUT_DIR, result_filename, 5, max_retries=12)
    result_file_path = os.path.join(OUTPUT_DIR, result_filename)
    external_id = await accounting_integration.parse_pohoda_xml(result_file_path)
    return {'external_id': external_id}

@app.post('/upload-expense-attachment')
async def upload_expense_attachment(request: Request):
    """Endpoint to upload an expense attachment."""
    try:
        data = await request.json()
        external_id = data.get('external_id')
        if not external_id:
            raise ValueError("Missing 'external_id' in request body")
        attachment_data = data.get('attachment')
        if not attachment_data:
            raise ValueError("Missing 'attachment' in request body")
        attachment = Attachment(**attachment_data)
        file_content = base64.b64decode(attachment.content)
        logger.debug(f'Attachment received for document: {attachment.document_name} and external_id: {external_id}')
        attachment_path = os.path.join(INPUT_DIR, attachment.document_name)
        with open(attachment_path, 'wb') as f:
            f.write(file_content)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f'Error processing attachment: {e}')
        raise HTTPException(status_code=400, detail='Error processing attachment')



