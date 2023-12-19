from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.authentication.models import Printer
from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer


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
                                 pay_on_collection=order_request["pay_on_collection"])

    order_serializer = OrderSerializer(instance=order)

    return Response(data={
        "data": order_serializer.data
    }, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_order_by_id(request: Request, order_id: int):

    order = Order.objects.get(id=order_id)
    order_serializer = OrderSerializer(instance=order)

    return Response(data={"data": order_serializer.data}, status=status.HTTP_200_OK)
