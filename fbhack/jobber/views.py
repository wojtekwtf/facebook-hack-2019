from django.shortcuts import render

def home(request):
    if request.method == 'POST':
        print(request.POST['job'])
        
    context = {}
    return render(request,'jobber/homepage.html',context)

# Create your views here.
