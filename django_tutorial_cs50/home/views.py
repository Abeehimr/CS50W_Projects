from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world!")

def greet(request,name:str):
    return render(request,"home/greet.html",{
        "name":name.capitalize()
    })