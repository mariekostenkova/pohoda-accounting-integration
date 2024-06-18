from datetime import datetime

from pydantic import BaseModel


class PaymentInformation(BaseModel):
    payment_method: str
    payment_amount: float
    payment_date: datetime
    currency: str


class Supplier(BaseModel):
    supplier_id: str
    supplier_name: str
    vat_number: str
    address: dict


class Address(BaseModel):
    street: str
    city: str
    postal_code: str
    country: str


class ExpenseDocument(BaseModel):
    document_id: str
    description: str
    date: str
    amount: float
    currency: str


class AttachmentMetadata(BaseModel):
    external_id: str
    record_id: str
    document_name: str


class Attachment(BaseModel):
    document_name: str
    content: str  # Base64-encoded file content
    content_type: str
    attachment_metadata: AttachmentMetadata
    attachment_binary: str


class FileStatus(BaseModel):
    result_status: str


class PartyIdentity(BaseModel):
    party_business_id: str
    party_name: str


class ExpenseDataInput(BaseModel):
    party_identity: PartyIdentity
    document_data: ExpenseDocument


class ExpenseDataResponse(BaseModel):
    external_id: str
