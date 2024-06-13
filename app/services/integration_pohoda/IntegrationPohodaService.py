import xml.etree.ElementTree as ET

class IntegrationPohodaService:
    pass


def transformation_json_to_xml(json_data, output_path: str) -> str:
    data_pack = ET.Element("dataPack", {
        "version": "2.0",
        "id": "import",
        "ico": json_data["ExpenseDataInput"]["party_identity"]["party_business_id"]
    })

    data_pack_item = ET.SubElement(data_pack, "dataPackItem", {"version": "2.0", "id": json_data["ExpenseDataInput"]["document_data"]["document_number"]})

    invoice = ET.SubElement(data_pack_item, "invoice", {"version": "2.0"})

    invoice_header = ET.SubElement(invoice, "invoiceHeader")
    ET.SubElement(invoice_header, "invoiceType").text = "issuedInvoice"
    ET.SubElement(invoice_header, "number").text = json_data["ExpenseDataInput"]["document_data"]["document_number"]
    ET.SubElement(invoice_header, "symVar").text = json_data["ExpenseDataInput"]["document_data"]["document_number"]
    ET.SubElement(invoice_header, "date").text = json_data["ExpenseDataInput"]["document_data"]["date_issue"]
    ET.SubElement(invoice_header, "dateTax").text = json_data["ExpenseDataInput"]["document_data"]["date_taxcontrol"]
    ET.SubElement(invoice_header, "dateDue").text = json_data["ExpenseDataInput"]["document_data"]["date_due"]





