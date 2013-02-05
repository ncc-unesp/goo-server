from django.shortcuts import render

def doc(request):
    context = {}
    return render(request,
                  'doc/index.phtml',
                  context)

# Create your views here.
