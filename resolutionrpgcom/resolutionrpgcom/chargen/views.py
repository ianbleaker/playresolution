from django.shortcuts import render


# Create your views here.

# INDEX #
# context is the character, send to index.html
def index(request):
    return render(request, 'chargen/index.html')
