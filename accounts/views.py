from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form}) 


@login_required
def home_view(request):

    if request.user.is_staff:
        return render(request, 'home_staff.html')  
    else:   
        return render(request, 'home.html')    
    
    