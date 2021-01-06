from django.shortcuts import render, redirect
from .forms import UserRegisterForm
# Flash messages are only displayed on a template once and disappear on the next request.
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            return render(request, 'users/register.html', {'form': form})

    else:
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})