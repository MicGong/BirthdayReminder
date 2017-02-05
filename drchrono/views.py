
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponse
from models import *

def main(request):
    print 'Redirect to main page with request: ', request
    return render(request, 'main.html')