from fastapi import FastAPI, UploadFile, File, HTTPException
import multiprocessing
import logging
import json
import os

from app.models import Attachment, ExpenseDocument
from app.services.integration_pohoda.IntegrationPohodaService import transformation_json_to_xml
from app.config import OUTPUT_PATH


app = FastAPI(title="Pohoda Accounting System Integration")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/upload-expense-attachment")
async def upload_expense_attachment(attachment: Attachment):
    return {"status_code": "200"}


@app.post("/upload-expense-data")
async def upload_expense_data():
    try:
        directory_path = OUTPUT_PATH
        json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]

        for json_file in json_files:
            file_path = os.path.join(directory_path, json_file)
            with open(file_path, 'r') as f:
                json_data = json.load(f)
                expense_document = ExpenseDocument(**json_data)

                input_file = os.path.splitext(json_file)[0] + ".xml"
                xml_filepath = transformation_json_to_xml(expense_document.dict(), input_file)

        return {"status": "Successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error processing files: {e}')


def execute_pohoda_command(user: str, password: str, input_filename: str):
  pass

def move_or_file_delete():
  pass

def count_worker():
    cpu_count = multiprocessing.cpu_count()
    workers = 2 * cpu_count
    return workers




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



