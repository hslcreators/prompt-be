from django.shortcuts import render

from django.http import HttpResponse, JsonResponse

# Create your views here.
def test(request, *args, **kwargs):
    return HttpResponse('<h1>Everything working fine!</h1>')