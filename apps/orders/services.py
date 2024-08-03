from apps.authentication.models import Printer
from apps.orders.models import OrderDocument
from apps.orders.serializers import OrderDocumentSerializer, OrderSerializer


def order_charge(printer: Printer, no_of_copies: int, pages: int, coloured: bool):

    if coloured:
        return no_of_copies * pages * printer.coloured_rate
    else:
        return no_of_copies * pages * printer.uncoloured_rate
    
def add_document_to_order_serializer_data(order_serializer: OrderSerializer, order_id: int):

    documents = OrderDocument.objects.filter(order_id=order_id)

    documents_serialized_list = []
    
    for document in documents:
        
        document_serializer = OrderDocumentSerializer(instance=document)

        documents_serialized_list.append(document_serializer.data["document"])

    response = order_serializer.data
    response.update({"documents": documents_serialized_list})

    return response

def convert_orders_to_response(orders):

    response = []

    for order in orders:

        order_serializer = OrderSerializer(instance=order)

        response.append(add_document_to_order_serializer_data(order_serializer, order.id))

    return response
