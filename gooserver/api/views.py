from django.http import HttpResponse
from django.shortcuts import render_to_response

# Create your views here.
def doc(request):
    template = 'api/doc.phtml'
    return render_to_response(template, {})
