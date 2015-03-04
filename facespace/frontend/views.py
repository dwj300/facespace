from django.shortcuts import render
from stronghold.decorators import public

# Create your views here.
@public
def index(request):
    return render(request, 'index.html')

#@login_required
def home(request):
	return render(request, 'home.html')