from uuid import UUID

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.authentication.models import Printer
from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer
from . import services


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_order(request: Request):
    order_request = request.data
    user = request.user
    printer_id = request.data["printer_id"]
    printer = Printer.objects.get(id=printer_id)

    order = Order.objects.create(user=user, printer=printer, document=order_request["document"],
                                 no_of_copies=order_request["no_of_copies"], pages=order_request["pages"],
                                 description=order_request["description"],
                                 time_expected=order_request["time_expected"],
                                 coloured=order_request["coloured"],
                                 pay_on_collection=order_request["pay_on_collection"])
    
    order.save()

    order_serializer = OrderSerializer(instance=order)

    return Response(data={
        "data": order_serializer.data
    }, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_order_by_id(request: Request, order_id: UUID):

    order = Order.objects.get(id=order_id)
    order_serializer = OrderSerializer(instance=order)

    return Response(data={"data": order_serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_orders_by_printer(request: Request):
    user = request.user
    printer = Printer.objects.get(id_user=user.id)

    orders = Order.objects.filter(printer=printer)
    order_serializer = OrderSerializer(instance=orders, many=True)

    return Response(data={"data": order_serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_orders_by_user(request: Request):
    user = request.user

    orders = Order.objects.filter(user=user)
    order_serializer = OrderSerializer(instance=orders, many=True)

    return Response(data={"data": order_serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_order_schedule(request: Request, order_id: UUID):

    order = Order.objects.get(id=order_id)
    order_serializer = OrderSerializer(instance=order)
    order_data = order_serializer.data

    charge = services.charge(order.no_of_copies, int(order.pages))

    if order.coloured:
        charge *= 50
    else:
        charge *= 20

    # TODO: ask how much these actually cost

    response = {
        "order_id": order_id,
        "pickup_time": order_data["time_expected"],
        "is_complete": order_data["is_complete"],
        "charge": charge,
        "paid": order_data["paid"]
    }

    return Response(data=response, status=status.HTTP_200_OK)


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
