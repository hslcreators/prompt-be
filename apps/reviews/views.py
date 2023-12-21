from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.authentication.models import Printer
from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer

# Create your views here.
@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_review(request: Request, *args, **kwargs):
    review_request = request.data
    user = request.user
    printer_id = review_request['printer_id']
    try:
        printer = Printer.objects.get(id=printer_id)
    except:
        return Response({'error': 'Invalid Printer ID'})
    
    new_review = Review.objects.create(user=user, printer=printer, rating=review_request['rating'],
                      comment=review_request['comment'], time_posted=review_request['time_posted'])
    
    new_review.save()
    
    review_serializer = ReviewSerializer(instance=new_review)
    
    return Response(data={
        "data": review_serializer.data
    }, status=status.HTTP_201_CREATED)
    

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_review_by_id(request: Request, review_id: int):

    review = Review.objects.get(id=review_id)
    review_serializer = ReviewSerializer(instance=review)

    return Response(data={"data": review_serializer.data}, status=status.HTTP_200_OK)
    