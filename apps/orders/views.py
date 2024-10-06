from uuid import UUID

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.authentication.models import Printer
from apps.orders.models import Order, OrderDocument
from apps.orders.requests import CreateOrderRequest, UpdateStatusRequest
from apps.orders.responses import OrderDocumentResponse, OrderResponse, OrderScheduleResponse, UpdateStatusResponse
from apps.orders.serializers import OrderDocumentSerializer, OrderSerializer
from . import services
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method='post', request_body=CreateOrderRequest(many=False), operation_id='Create Order', responses={201: OrderResponse(many=False)}
)
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_order(request: Request):
    order_request = request.data
    user = request.user
    documents = request.FILES.getlist("documents")
    printer_id = request.data["printer_id"]
    printer = Printer.objects.get(id=printer_id)

    charge = services.order_charge(printer, int(order_request["no_of_copies"]), int(order_request["pages"]),
                                   order_request["coloured"])

    order = Order.objects.create(user=user, printer=printer,
                                 no_of_copies=order_request["no_of_copies"], pages=order_request["pages"],
                                 description=order_request["description"],
                                 time_expected=order_request["time_expected"],
                                 coloured=order_request["coloured"],
                                 charge=charge)
    
    documents_serialized_list = []
    
    for document in documents:
    
        document_instance = OrderDocument.objects.create(
                order_id=order.id,
                document_name=document.name,
                document=document.read()
            )
        
        document_serializer = OrderDocumentSerializer(instance=document_instance)

        documents_serialized_list.append({"id": document_serializer.data["id"], "name": document_serializer.data["document_name"]})
        
        document_instance.save()

    order.save()

    order_serializer = OrderSerializer(instance=order)

    response = order_serializer.data
    response.update({"documents": documents_serialized_list})

    response = services.add_extra_details_to_order(response)

    return Response(response, status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    method='get', request_body=None, operation_id='Get Order By Id', responses={200: OrderResponse(many=False)}
)
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_order_by_id(request: Request, order_id: UUID):
    order = Order.objects.get(id=order_id)
    order_serializer = OrderSerializer(instance=order)

    response = services.add_document_and_extra_details_to_order_serializer_data(order_serializer)

    return Response(data=response, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get', request_body=None, operation_id='Get Order By Printer', responses={200: OrderResponse(many=True)}
)
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_orders_by_printer(request: Request):
    user = request.user
    printer = Printer.objects.get(id_user=user.id)

    orders = Order.objects.filter(printer=printer)

    response = services.convert_orders_to_response(orders)

    return Response(data=response, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get', request_body=None, operation_id='Get Order By User', responses={200: OrderSerializer(many=True)}
)
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_orders_by_user(request: Request):
    user = request.user

    orders = Order.objects.filter(user=user)

    response = services.convert_orders_to_response(orders)

    return Response(data=response, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get', request_body=None, operation_id='Get Order Schedule', responses={200: OrderScheduleResponse(many=False)}
)
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_order_schedule(request: Request, order_id: UUID):
    order = Order.objects.get(id=order_id)
    order_serializer = OrderSerializer(instance=order)
    order_data = order_serializer.data

    response = {
        "order_id": order_id,
        "pickup_time": order_data["time_expected"],
        "is_complete": order_data["is_complete"],
        "charge": order.charge,
        "paid": order_data["paid"]
    }

    return Response(data=response, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='put', request_body=UpdateStatusRequest(many=False), operation_id='Update Complete Status', responses={200: UpdateStatusResponse(many=False)}
)
@api_view(["PUT"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_complete_status(request: Request, order_id: UUID):
    user = request.user
    printer = Printer.objects.get(user=user)

    order = Order.objects.get(printer=printer, id=order_id)

    complete_status = request.data["is_complete"]
    order.is_complete = complete_status

    order.save()

    if order.is_complete:
        return Response({"data": "Order status has been set to completed"}, status=status.HTTP_200_OK)

    return Response({"data": "Order status has been set to incomplete"}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get', request_body=None, operation_id='Get Active Orders', responses={200: OrderResponse(many=True)}
)
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_active_orders(request: Request):
    user = request.user
    printer = Printer.objects.get(user=user)

    orders = Order.objects.filter(printer=printer, is_complete=False)

    response = services.convert_orders_to_response(orders)

    return Response(data=response, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get', request_body=None, operation_id='Get Order Document By Id', responses={200: OrderDocumentResponse(many=False)}
)
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_order_document_by_id(request: Request, order_document_id: int):

    try:
        return Response(data=services.get_order_document_by_id(request.user, order_document_id), status=status.HTTP_200_OK)
    except Exception:
        return Response(data={"message": "Order Document not found for user"})
