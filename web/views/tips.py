from django.shortcuts import redirect,render



def not_found(request):
    return render(request,'not_found.html')