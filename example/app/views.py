from django.shortcuts import render
from app.models import Checkbox

def savevalues(request):
    if request.method=='POST':
        if request.POST.get('coursename'):
            savedata=Checkbox()
            savedata.coursename = request.POST.get('coursename')
            savedata.save()
            return render(request, 'index.html')
    else:
        return render(request, 'index.html')