from uuid import UUID

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.authentication.models import Printer
from apps.orders.models import Order
from apps.orders.requests import CreateOrderRequest, UpdateStatusRequest
from apps.orders.responses import OrderScheduleResponse, UpdateStatusResponse
from apps.orders.serializers import OrderSerializer
from . import services
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method='post', request_body=CreateOrderRequest(many=False), operation_id='Create Order', responses={201: OrderSerializer(many=False)}
)
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_order(request: Request):
    order_request = request.data
    user = request.user
    printer_id = request.data["printer_id"]
    printer = Printer.objects.get(id=printer_id)

    charge = services.order_charge(printer, int(order_request["no_of_copies"]), int(order_request["pages"]),
                                   order_request["coloured"])

    order = Order.objects.create(user=user, printer=printer, document=order_request["document"],
                                 no_of_copies=order_request["no_of_copies"], pages=order_request["pages"],
                                 description=order_request["description"],
                                 time_expected=order_request["time_expected"],
                                 coloured=order_request["coloured"],
                                 charge=charge)

    order.save()

    order_serializer = OrderSerializer(instance=order)

    return Response(data=order_serializer.data, status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    method='get', request_body=None, operation_id='Get Order By Id', responses={200: OrderSerializer(many=False)}
)
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_order_by_id(request: Request, order_id: UUID):
    order = Order.objects.get(id=order_id)
    order_serializer = OrderSerializer(instance=order)

    return Response(data=order_serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get', request_body=None, operation_id='Get Order By Printer', responses={200: OrderSerializer(many=True)}
)
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_orders_by_printer(request: Request):
    user = request.user
    printer = Printer.objects.get(id_user=user.id)

    orders = Order.objects.filter(printer=printer)
    order_serializer = OrderSerializer(instance=orders, many=True)

    return Response(data=order_serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get', request_body=None, operation_id='Get Order By User', responses={200: OrderSerializer(many=True)}
)
@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_orders_by_user(request: Request):
    user = request.user

    orders = Order.objects.filter(user=user)
    order_serializer = OrderSerializer(instance=orders, many=True)

    return Response(data=order_serializer.data, status=status.HTTP_200_OK)

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


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_active_orders(request: Request):
    user = request.user
    printer = Printer.objects.get(user=user)

    orders = Order.objects.filter(printer=printer, is_complete=False)
    order_serializer = OrderSerializer(instance=orders, many=True)

    return Response(data=order_serializer.data, status=status.HTTP_200_OK)
