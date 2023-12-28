from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.authentication.models import Printer
from apps.orders.models import Order
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

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_reviews_for_me(request: Request):
    user = request.user
    
    if Printer.objects.filter(user=user).exists():
        printer = Printer.objects.get(user=user)
        
        reviews = Review.objects.filter(printer=printer)
    else:
        reviews = Review.objects.filter(user=user)
        
    review_serializer = ReviewSerializer(instance=reviews, many=True)
    
    return Response(data={"data": review_serializer.data}, status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_reviews_for_me(request: Request):
    user = request.user
    
    if Printer.objects.filter(user=user).exists():
        printer = Printer.objects.get(user=user)
        
        reviews = Review.objects.filter(printer=printer)
    else:
        reviews = Review.objects.filter(user=user)
        
    review_serializer = ReviewSerializer(instance=reviews, many=True)
    
    return Response(data={"data": review_serializer.data}, status=status.HTTP_200_OK)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_reviews(request: Request):
    printer_id = request.query_params.get("printer", None)
    
    if printer_id:
        try:
            printer = Printer.objects.get(id=int(printer_id))
        except:
            return Response({'error': 'Printer does not exist!'})
        
        reviews = Review.objects.filter(printer=printer).order_by('-time_posted')
    else:
        reviews = Review.objects.all()
        
    review_serializer = ReviewSerializer(instance=reviews, many=True)
    
    return Response(data={"data": review_serializer.data}, status=status.HTTP_200_OK)

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_review(request: Request, review_id):
    user = request.user
    
    review_data = request.data
    
    try:
        review = Review.objects.get(id=review_id, user=user)
    except:
        return Response({'error': 'Review does not exist!'})
    
    review.rating = review_data['rating']
    review.comment = review_data['comment']
    
    review.save()
    
    review_serializer = ReviewSerializer(instance=review)
    
    return Response(data={
        "data": review_serializer.data
    }, status=status.HTTP_200_OK)