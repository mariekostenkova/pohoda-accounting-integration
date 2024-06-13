from pydantic import BaseModel
import uuid

class PaymentInformation(BaseModel):
    payment_method: str
    amount: float
    currency: str

class Supplier(BaseModel):
    name: str
    vat_number: str
    address: dict

class Address(BaseModel):
    street: str
    city: str
    postal_code: str
    country: str

class ExpenseDocument(BaseModel):
    expense_type: str
    expense_document_description: str
    document_number: str
    payment_reference: str
    date_issue: str
    date_payment: str
    date_due: str
    date_taxcontrol: str
    payment: PaymentInformation
    supplier: Supplier
    place_of_purchase: Address
    accounting: str
    corroborative_invoice: bool
    record_id: uuid.UUID
    record_id_external: str
    record_created: str
    record_last_updated: str
    state: str
    source: str
    binary_file: str
    binary_file_filename: str
    binary_file_received: str
    binary_file_checksum: str
    binary_file_pdf: str
    binary_file_pdf_created: str
    document_plaintext: str
    llm_stats: dict
    client_specific_data: dict
    backlink_url: str
    harvest_problems: list
    harvested: bool
    document_content_warning: bool
class Attachment(BaseModel):
    document_id: str
    attachment: str
    external_id: str
    record_id: str
    document_name: str


class PartyIdentity(BaseModel):
    vat_tax_payer: bool
    restaurant: bool
    document: str
    party_business_id: str
    party_db_name: str


class FileStatus(BaseModel):
    result_status: str


class XmlData(BaseModel):
    pohoda_api: str
    user: str
    password: str
    input_filename: str


class ExpenseDataResponse(BaseModel):
    external_id: str