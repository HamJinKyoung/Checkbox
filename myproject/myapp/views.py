from django.shortcuts import render
from myapp.models import Option, Basket

# Create your views here.
def index(request):
    options = Option.objects
    if request.method=='POST':
        if request.POST.get('optionlist'):
            basket=Basket()
            basket.option_list = request.POST.get('optionlist')
            basket.ototal_price = request.POST['ototal']
            basket.save()
            return render(request, 'index.html', {'options':options})
    else:
        return render(request, 'index.html', {'options':options})