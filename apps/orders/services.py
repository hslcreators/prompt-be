from apps.authentication.models import Printer, User
from apps.orders.models import OrderDocument
from apps.orders.serializers import OrderDocumentSerializer, OrderSerializer

import zlib


def order_charge(printer: Printer, no_of_copies: int, pages: int, coloured: bool):

    if coloured:
        return no_of_copies * pages * printer.coloured_rate
    else:
        return no_of_copies * pages * printer.uncoloured_rate
    
def add_document_and_extra_details_to_order_serializer_data(order_serializer: OrderSerializer, order_id: int):

    order_documents = OrderDocument.objects.filter(order_id=order_id)

    documents_serialized_list = []
    
    for order_document in order_documents:
        
        document_serializer = OrderDocumentSerializer(instance=order_document)

        documents_serialized_list.append(document_serializer.data["document"])
        documents_serialized_list.append(document_serializer.data["document_name"])

    response = order_serializer.data
    response.update({"documents": documents_serialized_list})

    response = add_extra_details_to_order(response)

    return response

def convert_orders_to_response(orders):

    response = []

    for order in orders:

        order_serializer = OrderSerializer(instance=order)

        response.append(add_document_and_extra_details_to_order_serializer_data(order_serializer, order.id))

    return response

def add_extra_details_to_order(response: dict):
    printer_name = Printer.objects.get(id=response.get("printer")).print_service_name
    customer = User.objects.get(id=response.get("user"))
    customer_firstname = customer.first_name
    customer_lastname = customer.last_name

    customer_name = customer_firstname + " " + customer_lastname

    response.update({"customer_name": customer_name})
    response.update({"vendor_name": printer_name})

    return response

def compress_file_data(file_bytes):
    """Compress the file bytes."""
    return zlib.compress(file_bytes)

def decompress_file_data(compressed_data):
    """Decompress the file bytes."""
    return zlib.decompress(compressed_data)
