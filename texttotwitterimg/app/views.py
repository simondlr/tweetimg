# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from boto.s3.connection import S3Connection

def index(request):
    return HttpResponse('test')
